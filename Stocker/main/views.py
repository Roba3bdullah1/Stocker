from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product, Category, Supplier
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.utils.timezone import now
from django.db.models import Q, F
from datetime import timedelta
import json

def home_view(request):
    return render(request, 'main/home.html')

@login_required



def dashboard_view(request):
 
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()

    out_of_stock = Product.objects.filter(stock_quantity=0).count()
    low_stock = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lt=5).count()
    available = Product.objects.filter(stock_quantity__gte=5).count()
    discontinued = Product.objects.filter(status='discontinued').count()

    chart_data = json.dumps([available, out_of_stock, low_stock, discontinued])
    low_stock_products = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lt=5)

    today = now().date()
    expiry_threshold = today + timedelta(days=7)
    expired_products = Product.objects.filter(expiry_date__lt=today)

    expiring_soon_products = Product.objects.filter(expiry_date__gte=today, expiry_date__lte=expiry_threshold)

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'discontinued': discontinued,
        'available': available,
        'low_stock_products': low_stock_products,
        'expired_products': expired_products,
        'expiring_soon_products': expiring_soon_products,
        'chart_data': chart_data,
    }
    return render(request, 'main/dashboard.html', context)


def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('main:dashboard_view')
            else:
                return redirect('main:home_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            next_url = request.GET.get('next') or 'main:dashboard_view'  
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'main/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")
    return redirect('main:home_view') 

