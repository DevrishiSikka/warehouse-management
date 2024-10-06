from django.contrib import admin
from .models import Product, Category, Inventory

class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 1  # How many empty forms to display

class ProductAdmin(admin.ModelAdmin):
    inlines = [InventoryInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
