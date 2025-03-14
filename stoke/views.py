from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models import F, Sum
from django.core.mail import send_mail
from django.utils import timezone
from .models import Product, SoledProduct # Import your Product model
'''from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime'''


#========================================================================================================#
def login_view(request):
    """Handles user login."""
    if request.method == "POST":
        username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Thank you for logging in! You have logged in successfully.")
            return redirect('home')
        else:
            if not username or not password:
                messages.error(request, "Please provide both email and password.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password. Please try again.")
                return redirect('home')

    return render(request, 'store/index.html', {'title': 'Login'})
#========================================================================================================#

def logout_view(request):
    """Handles user logout."""
    logout(request)
    messages.info(request, "Goodbye! You have logged out successfully.")
    return redirect('home')
#========================================================================================================#

def create_account(request):
    """Placeholder for account creation logic."""
    return render(request, 'store/index.html', {'title': 'Create Account'})
#========================================================================================================#
def trigger_daily_report(request):
    send_daily_report()  # Call your existing function
    return HttpResponse("Daily report sent!")
def home(request):
    """Homepage view."""

    products = Product.objects.all()  # Query all products
    
    # Handle category filter
    category = request.GET.get('cateSelect', 'All')
    if category != 'All':
        products = products.filter(category=category)  # Filter by category
    
    # Handle search filter
    search_term = request.GET.get('searchBox', '')
    if search_term:
        products = products.filter(Q(name__icontains=search_term) | Q(card_id__icontains=search_term))  # Adjust the search fields if needed
    
    # Handle sorting
    sort_by = request.GET.get('sortSelect', '')
    if sort_by:
        if sort_by == 'Name':
            products = products.order_by('name')  # Sort by name (ascending)
        elif sort_by == 'Size':
            products = products.order_by('-product_number')  # Sort by product_number (descending)
        elif sort_by == 'Expired Date':
            products = products.order_by('expired_on')  # Sort by expired date (ascending)
    
    # Calculate days left for each product
    for product in products:
        if product.expired_on:
            expired_on = datetime.strptime(product.expired_on, "%Y-%m-%d")
            today = datetime.now()
            product.days_left = (expired_on - today).days
        else:
            product.days_left = None

    # Add some custom logic to calculate product metrics:
    sold_product = SoledProduct.objects.all()
    # 1. Total number of sold products
    total_sold = sold_product.aggregate(Sum('sold_number'))['sold_number__sum'] or 0  # Sum of sold_number (default to 0 if none)
    
    # 2. Get 5 most sold products
    most_sold_products = SoledProduct.objects.all().order_by('-sold_number')[:5]
    
    # 3. Products that need to be restocked
    restock_products = Product.objects.filter(product_number__lte=F('restock_threshold')).order_by('product_number')
    
    # 4. Expired products or soon-to-expire
    expired_products = Product.objects.filter(expired_on__lt=datetime.now()).order_by('expired_on')  # Expired products
    soon_expired_products = Product.objects.filter(expired_on__gt=datetime.now(), expired_on__lt=datetime.now() + timedelta(days=30)).order_by('expired_on')  # Expiring within 7 days
    
    # Pagination setup
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    product_page = paginator.get_page(page_number)
    
    return render(request, 'store/index.html', {
        'title': 'Home',
        'product_page': product_page,
        'category': category,
        'search_term': search_term,
        'sort_by': sort_by,
        'total_sold': total_sold,
        'most_sold_products': most_sold_products,
        'restock_products': restock_products,
        'expired_products': expired_products,
        'soon_expired_products': soon_expired_products,
    })

#========================================================================================================#
from django.core.mail import BadHeaderError

def send_daily_report():
    # Get today's date
    today = timezone.now().date()

    # Gather total number of sold products
    total_sold = SoledProduct.objects.aggregate(Sum('sold_number'))['sold_number__sum'] or 0  # Default to 0 if no data

    # Get the top 5 most sold products
    most_sold_products = SoledProduct.objects.all().order_by('-sold_number')[:5]

    # Products that need to be restocked based on last consumption
    restock_products = Product.objects.filter(product_number__lte=F('restock_threshold')).order_by('product_number')

    # Get expired products (expired today or before today)
    expired_products = Product.objects.filter(expired_on__lt=today).order_by('expired_on')

    # Get products that are about to expire in the next 30 days
    soon_expired_products = Product.objects.filter(
        expired_on__gt=today, 
        expired_on__lt=today + timedelta(days=30)
    ).order_by('expired_on')

    # Format the email content with HTML
    email_subject = f"Daily Product Report - {today}"
    
    email_body = f"""
    <html>
    <body>
        <h2>Daily Product Report for {today}</h2>
        
        <p><strong>Total Sold Products:</strong> {total_sold}</p>
        
        <h3>Top 5 Most Sold Products:</h3>
        <ul>
    """
    
    for product in most_sold_products:
        email_body += f"<li>{product.name}: {product.sold_number} units sold</li>"
    
    email_body += "</ul>"

    email_body += """
        <h3>Products Needing Restock:</h3>
        <ul>
    """
    
    for product in restock_products:
        email_body += f"<li>{product.name}: Current stock: {product.product_number}, Needs restock: {product.restock_threshold - product.product_number} units</li>"
    
    email_body += "</ul>"

    email_body += """
        <h3>Expired Products:</h3>
        <ul>
    """
    
    for product in expired_products:
        email_body += f"<li>{product.name}: Expired on {product.expired_on}</li>"
    
    email_body += "</ul>"

    email_body += """
        <h3>Products Expiring Soon (within 30 days):</h3>
        <ul>
    """
    
    for product in soon_expired_products:
        email_body += f"<li>{product.name}: Expiring on {product.expired_on}</li>"
    
    email_body += """
        </ul>
        <p>Kind regards,</p>
        <p>Your Stock Management Reporting System</p>
    </body>
    </html>
    """

    try:
        # Send the email with HTML content
        send_mail(
            email_subject,
            '',  # Body of the email is passed in the html format
            'lilianekamaliza790@gmail.com',  # Sender's email
            ['hakizayezudaniel@gmail.com', 'gigigenie99@gmail.com'],  # Recipient's email
            html_message=email_body,  # The HTML body of the email
            fail_silently=False,
        )
        print("Email sent successfully.")
    except BadHeaderError:
        print("Invalid header found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#========================================================================================================#

def add_product(request):
    """Placeholder for adding a product."""
    if request.method == "POST":
        # Extract form data from POST request
        category = request.POST.get('cateSelect')
        card_id = request.POST.get('deviceID')
        name = request.POST.get('deviceName')
        produced_at = request.POST.get('produced_at')
        expired_on = request.POST.get('product_expired')
        product_number = int(request.POST.get('number'))

        # Create a new product instance
        new_product = Product(
            category=category,
            card_id=card_id,
            name=name,
            produced_at=produced_at,
            expired_on=expired_on,
            product_number=product_number,
        )

        # Save the product instance to the database
        new_product.save()

        # Optionally, you can add a success message or redirect to a different page
        messages.success(request, "Item Added!.")
        return redirect('home')
    return render(request, 'store/index.html', {'title': 'Add Product'})
#========================================================================================================#

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product  # Assuming you have a Product model

def remove_product(request):
    """Remove or update product quantity in the store inventory."""
    if request.method == 'POST':
        # Get the form data
        product_name = request.POST.get('deviceName')
        card_id = request.POST.get('deviceID')
        quantity_to_remove = int(request.POST.get('number'))  # Convert to int for comparison
        expiration_date = request.POST.get('product_expired')

        # Get the product to be removed
        product = get_object_or_404(Product, name=product_name, card_id=card_id)

        if product:

            # Check if the quantity to remove is valid
            if quantity_to_remove > product.product_number:
                # If the quantity to remove is greater than what's in stock, return an error message
                messages.error(request, f"Error: Stock is low. Only {product.product_number} available.")
            elif quantity_to_remove < product.product_number:
               
                # Try to get the SoldProduct entry, if it exists
                sold_product, created = SoledProduct.objects.get_or_create(card_id=product.card_id)
                if created:
                    # If this is a new product in SoldProduct, create the new entry
                    sold_product.sold_number = quantity_to_remove
                    sold_product.name = product.name
                    sold_product.save()
                    #messages.success(request, f"{quantity_to_remove} of {product_name} added to sold products!")

                else:
                    # If the product is already in SoldProduct, update the sold number
                    sold_product.sold_number += quantity_to_remove
                    sold_product.save()

                    # Move this row to the "last" position (if we are ordering by created_at or another field)
                    # Assuming `created_at` exists on SoldProduct and we want to move the product to the latest position
                    sold_product.refresh_from_db()  # Ensure we're working with the latest DB state
                    sold_product.save()

                    #messages.success(request, f"Updated sold quantity for {product_name} to {sold_product.sold_number}!")

                # If the quantity to remove is less than the stock, subtract it from the stock
                product.product_number -= quantity_to_remove
                product.save()
                messages.success(request, f"{quantity_to_remove} of {product_name} removed successfully!")
            else:  # If the quantity to remove is exactly equal to the stock

                # Try to get the SoldProduct entry, if it exists
                sold_product, created = SoledProduct.objects.get_or_create(card_id=product.card_id)
                if created:
                    # If this is a new product in SoldProduct, create the new entry
                    sold_product.sold_number = quantity_to_remove
                    sold_product.name = product.name
                    sold_product.save()

                else:
                    # If the product is already in SoldProduct, update the sold number
                    sold_product.sold_number += quantity_to_remove
                    sold_product.save()
                    
                    # Move this row to the "last" position (if we are ordering by created_at or another field)
                    # Assuming `created_at` exists on SoldProduct and we want to move the product to the latest position
                    sold_product.refresh_from_db()  # Ensure we're working with the latest DB state
                    sold_product.save()

                # Delete the product if the quantity is exactly the same
                product.delete()
                messages.success(request, f"All of {product_name} removed successfully!")
        else:
            messages.error(request, f"No product of this ID: {product.card_id}")

        # Redirect back to the store page or wherever needed
        return redirect('home')  # Make sure you update this with the correct URL name
    else:
        return render(request, 'store/index.html', {'title': 'Remove Product'})

#========================================================================================================#
rfid_id = None
def handle(request):
    global rfid_id  # Reference the global variable
    try:
        if request.method == "GET":
            rfid_id1 = request.GET.get('rfid_id')
            print("Received RFID ID:", rfid_id1)  # Check what we receive
            
            #rfid_id1 = '5EC7DE6B'

            if (rfid_id1):
                rfid_id = rfid_id1
                esp_url = f"http://192.168.8.101:8000/get_product_details/?rfid_id={rfid_id1}"
                return JsonResponse({'url': esp_url})

            elif rfid_id:
                try:
                    # Convert rfid_id1 to an integer
                    rfid_id = int(rfid_id,16)
                    print("Received RFID ID1:", rfid_id)  # Check what we receive
                except ValueError:
                    return JsonResponse({'error': 'Invalid RFID ID format. It must be an integer.'}, status=400)

                # Dynamically create the URL for the product details
                print("Received RFID:", rfid_id)  # Check what we receive
                esp_url = f"http://192.168.8.101:8000/get_product_details/?rfid_id={rfid_id}"
                print("Generated URL:", esp_url)
                return JsonResponse({'url': esp_url})
            
            else:
                # If no rfid_id is received, ask the user to try again
                return JsonResponse({'error': 'No RFID ID provided'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
#========================================================================================================#

def get_product_details(request):
    print("Gud")
    try:
        if request.method == "GET":
            rfid_id = request.GET.get('rfid_id')
        
            if not rfid_id:
                return JsonResponse({"error": "No RFID ID provided"}, status=400)

            #product = Product.objects.filter(card_id=rfid_id).first()
            product = Product.objects.filter(card_id=rfid_id).first()

            if product:
                print("Product Exit", product.name,product.card_id,product.expired_on)
                return JsonResponse({
                    "exists": True,
                    "message": "Product found. Show Remove Product form.",
                    "rfid_id": product.card_id,
                    "deviceName": product.name,
                    "product_expired": product.expired_on,
                    "product_number": product.product_number
                    #"product_expired": product.expired_on.strftime("%Y-%m-%d") if product.expired_on else "N/A",
                    
                })
            else:
                return JsonResponse({
                    "exists": False,
                    "message": "Product not found. Show Add Product form.",
                    "rfid_id": rfid_id,
                })
        else:
            return JsonResponse({"error": "Invalid request method. Use GET."}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
