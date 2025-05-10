from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import ProductType, ProductInstance, Category
from .forms import ProductForm
from django.http import JsonResponse

# فرم ایجاد محصول جدید
class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ['product_type', 'total_weight', 'unit', 'price_per_kilo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit'].widget.attrs.update({'class': 'form-control'})
        self.fields['price_per_kilo'].widget.attrs.update({'class': 'form-control'})

@login_required
def product_list(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Associate the product with the current user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    
    # Filter products by the current user
    products = ProductInstance.objects.filter(user=request.user).order_by('-created_at')
    
    # Get all product types for JavaScript unit mapping
    product_types = ProductType.objects.all()
    
    context = {
        'form': form,
        'products': products,
        'product_types': product_types,
    }
    return render(request, 'core/product_list.html', context)

@method_decorator(login_required, name='dispatch')
class ProductTypeListView(ListView):
    model = ProductType
    template_name = 'core/product_type_list.html'
    context_object_name = 'product_types'

def get_product_type_unit(request):
    """
    AJAX view to return the unit for a given product type
    """
    product_type_id = request.GET.get('id')
    if not product_type_id:
        return JsonResponse({'error': 'No product type ID provided'}, status=400)
    
    try:
        product_type = ProductType.objects.get(id=product_type_id)
        return JsonResponse({'unit': product_type.unit})
    except ProductType.DoesNotExist:
        return JsonResponse({'error': 'Product type not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
