from django.contrib import admin
from .models import Product, SoledProduct

class ProductCarAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'category', 'name', 'product_number', 'produced_at', 'expired_on')
    search_fields = ('card_id', 'category', 'name')
    list_filter = ('category',)

class SoledProductCarAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'name', 'sold_number')
    search_fields = ('card_id', 'name')
    #list_filter = ('category',)

# Register your models here.
admin.site.register(Product, ProductCarAdmin)
admin.site.register(SoledProduct, SoledProductCarAdmin)
