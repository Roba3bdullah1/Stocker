from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product, Stock, Category, Supplier
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

def home_view(request):
    return render(request, 'main/home.html')

@login_required
def dashboard_view(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    out_of_stock = Stock.objects.filter(quantity=0).count()
    low_stock = Stock.objects.filter(quantity__range=(1,4)).count()

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
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
    messages.success(request, "Logged out successfully!")
    return redirect('main:login_view') 