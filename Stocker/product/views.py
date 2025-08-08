from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .models import Product
from .forms import ProductForm
from .models import Supplier
from .forms import SupplierForm
from .models import Category
from .forms import CategoryForm
from django.core.paginator import Paginator
from django.db.models import Q




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
    return render(request, 'product/update_product.html', {'form': form})


 

def delete_product_view(request:HttpRequest,pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products_list_view')

    return render(request, 'product/product_confirm_delete.html', {'product': product})
 

def products_list_view(request:HttpRequest):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})



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
    paginator = Paginator(suppliers, 10)  # 10 لكل صفحة
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
            return redirect('supplier_list_view') 
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
            return redirect('supplier_list_view')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'product/supplier_form.html', {'form': form})

def delete_supplier_view(request:HttpRequest, pk):
    supplier = Supplier.objects.get(pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list_view')
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
            return redirect('product:category_list_view')
    else:
        form = CategoryForm()
    return render(request, 'product/category_form.html', {'form': form})


def update_category_view(request:HttpRequest, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('product:category_list_view')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'product/category_form.html', {'form': form})


def delete_category_view(request:HttpRequest, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('product:category_list_view')
    return render(request, 'product/category_confirm_delete.html', {'category': category})




def stock_update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    stock, created = Stock.objects.get_or_create(product=product)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('product:product_detail_view', pk=product.id)
    else:
        form = StockForm(instance=stock)

    return render(request, 'product/stock_form.html', {
        'form': form,
        'product': product,
    })