from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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
from django.utils import timezone
from django.db.models import Sum
import json
from django.db.models import Count
import csv
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime, timedelta


def add_product_view(request: HttpRequest):
    if not (request.user.is_staff and request.user.has_perm("product.add_product")):
        messages.warning(request, "Only admins can add products.", "alert-warning")
        return redirect('product:products_list_view')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('product:products_list_view')
    else:
        form = ProductForm()
    return render(request, 'product/add_product.html', {'form': form})

from datetime import datetime, timedelta
from django.utils import timezone

def update_product_view(request: HttpRequest, pk):
    if not (request.user.is_staff and request.user.has_perm("product.change_product")):
        messages.warning(request, "Only admins can update products.", "alert-warning")
        return redirect('product:products_list_view')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)

        
            if product.stock_quantity == 0:
                product.status = 'out_of_stock'
            elif product.stock_quantity < product.LOW_STOCK_THRESHOLD:
                product.status = 'low_stock'
            else:
                product.status = 'available'

            product.save()
            messages.success(request, "Product updated successfully!")
            

            send_email = False
            expiry_date = None

            today = timezone.now().date()
            alert_date = today + timedelta(days=7)  

            if product.stock_quantity <= product.LOW_STOCK_THRESHOLD:
                send_email = True

            if product.expiry_date:
              
                if today <= product.expiry_date <= alert_date:
                    send_email = True
                    expiry_date = product.expiry_date

            
                if product.expiry_date < today:
                    send_email = True
                    expiry_date = product.expiry_date

            if send_email:
                send_alert_email(product.name, product.stock_quantity, expiry_date)

            return redirect('product:products_list_view')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product/update_product.html', {'form': form, 'product': product})

 

def delete_product_view(request, pk):
    if not (request.user.is_staff and request.user.has_perm("product.delete_product")):
        messages.warning(request, "Only admins can delete products.", "alert-warning")
        return redirect('product:products_list_view')
    
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully.")
        return redirect('product:products_list_view')
    return redirect('product:products_list_view',{'product': product} )
 

def products_list_view(request):
    search_query = request.GET.get('q', '')  
    selected_category = request.GET.get('category', '')
    selected_supplier = request.GET.get('supplier', '')  
    selected_status = request.GET.get('status', '')

    products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)

    if selected_category:
        products = products.filter(category__id=selected_category)

    if selected_supplier:
        products = products.filter(supplier__id=selected_supplier)

    if selected_status:
        products = products.filter(status=selected_status)

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    context = {
        'products': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'paginator': paginator,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_supplier': selected_supplier,
        'selected_status': selected_status,
        'categories': categories,
        'suppliers': suppliers,
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
    paginator = Paginator(suppliers, 2) 
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
    if not (request.user.is_staff and request.user.has_perm("product.add_supplier")):
        messages.warning(request, "Only admins can add suppliers.", "alert-warning")
        return redirect('product:suppliers_list_view')

    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier added successfully!")
            return redirect('product:suppliers_list_view') 
    else:
        form = SupplierForm()
    return render(request, 'product/supplier_form.html', {'form': form})

def supplier_detail_view(request:HttpRequest, pk):
    supplier = Supplier.objects.get(pk=pk)
    products = supplier.product_set.all()  
    return render(request, 'product/supplier_detail.html', {'supplier': supplier,'products': products,})

def update_supplier_view(request:HttpRequest,pk):
    if not (request.user.is_staff and request.user.has_perm("product.change_supplier")):
        messages.warning(request, "Only admins can update suppliers.", "alert-warning")
        return redirect('product:suppliers_list_view')
     
    supplier = Supplier.objects.get(pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier updated successfully!")
            return redirect('product:suppliers_list_view')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'product/supplier_form.html', {'form': form})

def delete_supplier_view(request:HttpRequest, pk):
    if not (request.user.is_staff and request.user.has_perm("product.delete_supplier")):
        messages.warning(request, "Only admins can delete suppliers.", "alert-warning")
        return redirect('product:suppliers_list_view')
    
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
    paginator = Paginator(categories, 2) 
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
            messages.success(request, "Category added successfully!")
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
            messages.success(request, "Category updated successfully!")
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



def update_stock_view(request, product_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_stock = int(data.get('stock', -1))
            if new_stock < 0:
                return JsonResponse({'success': False, 'error': 'Invalid stock value'})

            product = Product.objects.get(id=product_id)
            product.stock_quantity = new_stock

            #
            if new_stock == 0:
                product.status = 'out_of_stock'
            elif new_stock < product.LOW_STOCK_THRESHOLD:
                product.status = 'low_stock'
            else:
                product.status = 'available'

            product.save()

           
            if product.status == 'out_of_stock':
                stock_status = 'Out of Stock'
            elif product.status == 'low_stock':
                stock_status = 'Low Stock'
            else:
                stock_status = 'Available'

            return JsonResponse({'success': True, 'status': stock_status})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
 
def inventory_report_view(request):
    category_id = request.GET.get('category')
    supplier_id = request.GET.get('supplier')
    status = request.GET.get('status')

    products = Product.objects.all().order_by('name')  

    if category_id:
        products = products.filter(category_id=category_id)
    if supplier_id:
        products = products.filter(supplier_id=supplier_id)
    if status:
        products = products.filter(status=status)

    today = timezone.now().date()

    total_products = products.count()
    available_count = products.filter(status='available').count()
    low_stock_count = products.filter(status='low_stock').count()
    out_of_stock_count = products.filter(status='out_of_stock').count()
    discontinued_count = products.filter(status='discontinued').count()
    expired_count = products.filter(expiry_date__lt=today).count()

    categories = Category.objects.all()
    suppliers = Supplier.objects.all()

    context = {
        'products': products,
        'total_products': total_products,
        'available_count': available_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'discontinued_count': discontinued_count,
        'expired_count': expired_count,
        'categories': categories,
        'suppliers': suppliers,
        'selected_category': category_id,
        'selected_supplier': supplier_id,
        'selected_status': status,
    }
    return render(request, 'product/inventory_report.html', context)


def export_csv_view(request):
    category_id = request.GET.get('category')
    supplier_id = request.GET.get('supplier')
    status = request.GET.get('status')

    print(f"Received filters - category: {category_id}, supplier: {supplier_id}, status: {status}")

    products = Product.objects.all()

    if category_id and category_id.isdigit():
        products = products.filter(category_id=int(category_id))

    if supplier_id and supplier_id.isdigit():
        products = products.filter(supplier_id=int(supplier_id))

    if status:
        products = products.filter(status=status)

    products = products.order_by('name')

    print(f"Filtered products count: {products.count()}")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Category', 'Supplier', 'Status', 'Stock Quantity', 'Expiry Date', 'Price'])

    for p in products:
        writer.writerow([
            p.id,
            p.name,
            p.category.name if p.category else '',
            p.supplier.name if p.supplier else '',
            p.status,
            p.stock_quantity,
            p.expiry_date.strftime('%Y-%m-%d') if p.expiry_date else '',
            p.price,
        ])

    return response

def supplier_report_view(request):
    active = request.GET.get('active')
    suppliers = Supplier.objects.annotate(products_count=Count('product'))

    if active == 'yes':
        suppliers = suppliers.filter(products_count__gt=0)
    elif active == 'no':
        suppliers = suppliers.filter(products_count=0)

    today = timezone.now().date()
    products = Product.objects.all()

    available_count = products.filter(status='available').count()
    low_stock_count = products.filter(status='low_stock').count()
    out_of_stock_count = products.filter(status='out_of_stock').count()
    discontinued_count = products.filter(status='discontinued').count()
    expired_count = products.filter(expiry_date__lt=today).count()

    context = {
        'suppliers': suppliers,
        'selected_active': active,
        'available_count': available_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'discontinued_count': discontinued_count,
        'expired_count': expired_count,
    }
    return render(request, 'product/supplier_report.html', context)



def send_alert_email(product_name, stock_quantity, expiry_date=None):
    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        return

    context = {
        "product_name": product_name,
        "stock_quantity": stock_quantity,
        "expiry_date": expiry_date,
    }

    content_html = render_to_string("product/alert_email.html", context)
    email_message = EmailMessage(
        subject="Inventory Stock Alert",
        body=content_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[superuser.email],
    )
    email_message.content_subtype = "html"
    email_message.send()