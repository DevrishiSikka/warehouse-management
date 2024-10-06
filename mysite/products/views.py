from django.shortcuts import render
from .models import Product, Inventory

def product_list(request):
    products = Product.objects.all()
    return render(request, 'productList.html', {'products': products})
