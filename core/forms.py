from django import forms
from django.contrib.auth.models import User
from typing import Any, Dict, Optional, Callable

from .models import ProductInstance, ProductType, Recipe, RecipeItem


class ProductForm(forms.ModelForm):
    """
    Form for creating and editing product instances.
    """
    class Meta:
        model = ProductInstance
        fields = ['product_type', 'total_weight', 'unit', 'price_per_kilo']
        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the form and add Bootstrap classes to form fields.
        """
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class RecipeForm(forms.ModelForm):
    """
    Form for creating and editing recipes.
    """
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'selling_price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'نام غذا را وارد کنید'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'توضیحات غذا را وارد کنید'
            }),
            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'قیمت فروش'
            })
        }


class RecipeItemForm(forms.ModelForm):
    """
    Form for adding ingredients to a recipe.
    """
    class Meta:
        model = RecipeItem
        fields = ['product_instance', 'quantity']
        widgets = {
            'product_instance': forms.Select(attrs={
                'class': 'form-control recipe-product-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01', 
                'min': '0'
            })
        }
    
    def __init__(self, user: Optional[User] = None, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the form with user-specific product instances.
        
        Args:
            user: The user whose products should be displayed in the dropdown
        """
        super().__init__(*args, **kwargs)
        if user:
            # Only show products belonging to the current user
            self.fields['product_instance'].queryset = ProductInstance.objects.filter(user=user)
            
            # Modify how products are displayed in the dropdown - show only product name
            self.fields['product_instance'].label_from_instance = self.label_from_instance
    
    @staticmethod
    def label_from_instance(obj: ProductInstance) -> str:
        """
        Custom display method for product instances in dropdown.
        
        Args:
            obj: The product instance object
            
        Returns:
            The formatted display string for the dropdown
        """
        return f"{obj.product_type.name}" 
    