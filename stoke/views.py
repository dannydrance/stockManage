from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import Q
from .models import Product  # Import your Product model

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

def home(request):
    """Homepage view."""
    products = Product.objects.all()  # Query all products
    
    # Handle category filter
    category = request.GET.get('cateSelect', 'All')
    if category != 'All':
        products = products.filter(category=category)  # Filter by category
    #elif category == 'All':
        #products = Product.objects.all()  # Query all products 

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
        #elif sort_by == 'Sort By':
            #products = Product.objects.all()  # Query all products
            
    # Calculate days left for each product
    for product in products:
        if product.expired_on:
            if isinstance(product.expired_on, str):
                expired_on = datetime.strptime(product.expired_on, "%Y-%m-%d")
            else:
                expired_on = product.expired_on

            today = datetime.now()
            product.days_left = (expired_on - today).days
        else:
            product.days_left = None

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
    })

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
                # If the quantity to remove is less than the stock, subtract it from the stock
                product.product_number -= quantity_to_remove
                product.save()
                messages.success(request, f"{quantity_to_remove} of {product_name} removed successfully!")
            else:  # If the quantity to remove is exactly equal to the stock
                # Delete the product if the quantity is exactly the same
                product.delete()
                messages.success(request, f"All of {product_name} removed successfully!")
        else:
            messages.error(request, f"No roduct of this ID: {product.card_id}")

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
