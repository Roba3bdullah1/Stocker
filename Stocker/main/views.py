from django.shortcuts import render, redirect,render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product, Category, Supplier
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User
import json
from django.contrib import messages
from django.db.models import Count
from django.utils.timezone import now
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

    top_suppliers = Supplier.objects.annotate(product_count=Count('product')).order_by('-product_count')[:5]
    supplier_labels = [supplier.name for supplier in top_suppliers]
    supplier_counts = [supplier.product_count for supplier in top_suppliers]

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
        'supplier_labels': json.dumps(supplier_labels),
        'supplier_counts': json.dumps(supplier_counts),
    }
    return render(request, 'main/dashboard.html', context)



def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists","alert-danger")
            return redirect('main:signup_view')

        new_user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
        messages.success(request, "Registered User Successfully", "alert-success")
        return redirect('main:login_view')
           
    return render(request, 'main/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next') or 'main:dashboard_view'  
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'main/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('main:home_view') 



