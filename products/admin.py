from django.contrib import admin
from products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category', 'date_updated']
    search_fields = ['name', 'sku']
    list_filter = ('category',)
    prepopulated_fields = {"slug": ("name",)}

# reorder the model elements in the admin portal (may have to be done on the model page) to make logical sense.

# hide slug in admin portal, and have it update if the name is changed