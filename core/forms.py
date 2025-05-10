from django import forms
from .models import ProductInstance, ProductType

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ['product_type', 'total_weight', 'price_per_kilo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to the form fields
        self.fields['product_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['price_per_kilo'].widget.attrs.update({'class': 'form-control'}) 