from django import forms
from .models import Product
from .models import Supplier
from .models import Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'supplier', 'price', 'image']



class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name','logo', 'email','website', 'phone', 'address']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']