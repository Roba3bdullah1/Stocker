from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .models import Product
from .forms import ProductForm
from .models import Supplier
from .forms import SupplierForm
from .models import Category
from .forms import CategoryForm


def add_product_view(request: HttpRequest):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_list_view')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})


def update_product_view(request:HttpRequest,pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list_view')
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



def supplier_list_view(request:HttpRequest):
    suppliers = Supplier.objects.all()
    return render(request, 'product/supplier_list.html', {'suppliers': suppliers})




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





def category_list_view(request:HttpRequest):
    categories = Category.objects.all()
    return render(request, 'product/category_list.html', {'categories': categories})


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
