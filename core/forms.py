from django import forms
from .models import ProductInstance, ProductType, Recipe, RecipeItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ['product_type', 'total_weight', 'unit', 'price_per_kilo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to the form fields
        self.fields['product_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit'].widget.attrs.update({'class': 'form-control'})
        self.fields['price_per_kilo'].widget.attrs.update({'class': 'form-control'})

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'selling_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام غذا را وارد کنید'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'توضیحات غذا را وارد کنید'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'قیمت فروش'})
        }

class RecipeItemForm(forms.ModelForm):
    class Meta:
        model = RecipeItem
        fields = ['product_instance', 'quantity']
        widgets = {
            'product_instance': forms.Select(attrs={'class': 'form-control recipe-product-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'})
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # فقط محصولات کاربر جاری را نمایش بده
            self.fields['product_instance'].queryset = ProductInstance.objects.filter(user=user)
            
            # تغییر نحوه نمایش محصولات در منوی کشویی - فقط نام محصول
            self.fields['product_instance'].label_from_instance = self.label_from_instance
    
    @staticmethod
    def label_from_instance(obj):
        # فقط نام محصول را نمایش می‌دهد
        return f"{obj.product_type.name}" 