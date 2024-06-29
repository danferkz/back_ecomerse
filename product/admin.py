from django.contrib import admin
from .models import Product, Category

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'price',
        'quantity',
        'available',
        'reduced_image',
    )
    list_filter = ('available', 'price', 'category')
    search_fields = ('name', 'description')
    ordering = ('-date_added',)

admin.site.register(Product, ProductAdmin)

admin.site.register(Category)