from django.contrib import admin
from .models import Category, Supplier, Stock, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'website')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'price', 'created_at')
    search_fields = ('name',)
    list_filter = ('category', 'supplier')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'last_updated', 'is_low_stock', 'is_out_of_stock', 'is_expired')
    list_filter = ('last_updated',)

    def is_low_stock(self, obj):
        return obj.is_low_stock()
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock?'

    def is_out_of_stock(self, obj):
        return obj.is_out_of_stock()
    is_out_of_stock.boolean = True
    is_out_of_stock.short_description = 'Out of Stock?'

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired?'
