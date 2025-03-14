from django.contrib import admin
from .models import Product, SoledProduct

# Register your models here.
admin.site.register(Product)
admin.site.register(SoledProduct)
