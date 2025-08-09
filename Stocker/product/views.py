from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from .models import Supplier
from .forms import SupplierForm
from .models import Category
from .forms import CategoryForm
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from django.utils import timezone
from django.db.models import Sum


def add_product_view(request: HttpRequest):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product:products_list_view')
    else:
        form = ProductForm()
    return render(request, 'product/add_product.html', {'form': form})


def update_product_view(request:HttpRequest,pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product:products_list_view')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/update_product.html', {'form': form, 'product': product})


 

def delete_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully.")
        return redirect('product:products_list_view')
    return redirect('product:products_list_view',{'product': product} )
 

def products_list_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'product/product_list.html', context)


def product_detail_view(request:HttpRequest,pk):
    product = Product.objects.get(pk=pk)

    return render(request, 'product/product_detail.html', {'product': product})



def suppliers_list_view(request):
    query = request.GET.get('q', '')
    suppliers = Supplier.objects.all()
    if query:
        suppliers = suppliers.filter(
            Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query)
        )
    paginator = Paginator(suppliers, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'suppliers': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'product/suppliers_list.html', context)


def add_supplier_view(request:HttpRequest):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:suppliers_list_view') 
    else:
        form = SupplierForm()
    return render(request, 'product/supplier_form.html', {'form': form})

def supplier_detail_view(request:HttpRequest, pk):
    supplier = Supplier.objects.get(pk=pk)
    products = supplier.product_set.all()  
    return render(request, 'product/supplier_detail.html', {'supplier': supplier,'products': products,})

def update_supplier_view(request:HttpRequest,pk):
    supplier = Supplier.objects.get(pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('product:suppliers_list_view')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'product/supplier_form.html', {'form': form})

def delete_supplier_view(request:HttpRequest, pk):
    supplier = Supplier.objects.get(pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('suppliers_list_view')
    return render(request, 'product/supplier_confirm_delete.html', {'supplier': supplier})



def categories_list_view(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    if query:
        categories = categories.filter(Q(name__icontains=query) | Q(description__icontains=query))
    paginator = Paginator(categories, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'categories': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'product/category_list.html', context)


def add_category_view(request:HttpRequest):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:categories_list_view')
    else:
        form = CategoryForm()
    return render(request, 'product/category_form.html', {'form': form})


def update_category_view(request:HttpRequest, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('product:categories_list_view')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'product/category_form.html', {'form': form})


def delete_category_view(request:HttpRequest, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('product:category_list_view')
    return render(request, 'product/category_confirm_delete.html', {'category': category})



def stock_management_view(request):
    stocks = Stock.objects.select_related('product').all()

    low_stock_items = [i for i in stocks if i.is_low_stock()]
    expired_items = [i for i in stocks if i.is_expired()]

    context = {
        'stocks': stocks,
        'low_stock_items': low_stock_items,
        'expired_items': expired_items,
    }
    return render(request, 'product/stock_management.html', context)

def update_stock_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        new_quantity = request.POST.get('stock_quantity')
        if new_quantity.isdigit():
            product.stock_quantity = int(new_quantity)
            product.save()
            messages.success(request, f'Stock updated for {product.name}')
            return redirect('product:products_list_view')
        else:
            messages.error(request, 'Please enter a valid number.')
    
    return render(request, 'product/update_stock.html', {'product': product})

def stock_report_view(request):
    total_products = Stock.objects.count()
    total_quantity = Stock.objects.aggregate(total=Sum('quantity'))['total'] or 0
    low_stock_count = Stock.objects.filter(quantity__lt=Stock.LOW_STOCK_THRESHOLD).count()
    expired_count = Stock.objects.filter(expiry_date__lt=timezone.now().date()).count()

    context = {
        'total_products': total_products,
        'total_quantity': total_quantity,
        'low_stock_count': low_stock_count,
        'expired_count': expired_count,
    }
    return render(request, 'product/stock_report.html', context)