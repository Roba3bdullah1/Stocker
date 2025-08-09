from . import views
from django.urls import path

app_name = 'product'

urlpatterns = [

    path('products/', views.products_list_view, name='products_list_view'),
    path('products/<int:pk>/', views.product_detail_view, name='product_detail_view'),
    path('products/add/', views.add_product_view, name='add_product_view'),
    path('products/<int:pk>/update/', views.update_product_view, name='update_product_view'),
    path('products/delete/<int:pk>/', views.delete_product_view, name='delete_product_view'),

    path('suppliers/', views.suppliers_list_view, name='suppliers_list_view'),
    path('suppliers/add/', views.add_supplier_view, name='add_supplier_view'),
    path('suppliers/<int:pk>/', views.supplier_detail_view, name='supplier_detail_view'),
    path('suppliers/<int:pk>/update/', views.update_supplier_view, name='update_supplier_view'),
    path('suppliers/<int:pk>/delete/', views.delete_supplier_view, name='delete_supplier_view'),

    path('categories/', views.categories_list_view, name='categories_list_view'),
    path('categories/add/', views.add_category_view, name='add_category_view'),
    path('categories/<int:pk>/update/', views.update_category_view, name='update_category_view'),
    path('categories/<int:pk>/delete/', views.delete_category_view, name='delete_category_view'),

    path('stock/', views.stock_management_view, name='stock_management_view'),
    path('stock/update/<int:pk>/', views.update_stock_view, name='update_stock_view'),
    path('stock/report/', views.stock_report_view, name='stock_report_view'),



]


    