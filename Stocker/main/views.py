from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from product.models import Product,Stock

def home_view(request:HttpRequest):
    return render(request,'main/home.html')


def dashboard_view(request:HttpRequest):
    total_products = Product.objects.count()
    out_of_stock = Stock.objects.filter(quantity=0).count()
    low_stock = Stock.objects.filter(quantity__lt=5, quantity__gt=0).count()

    return render(request, 'main/dashboard.html', {'total_products': total_products,'out_of_stock': out_of_stock,'low_stock': low_stock})