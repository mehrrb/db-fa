from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django import forms
from .models import ProductType, ProductInstance

# فرم ایجاد محصول جدید
class ProductInstanceForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ['product_type', 'total_weight', 'price_per_kilo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['total_weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['price_per_kilo'].widget.attrs.update({'class': 'form-control'})

# Create your views here.
def product_list(request):
    products = ProductInstance.objects.all().select_related('product_type')
    product_types = ProductType.objects.all()
    
    # اگر درخواست POST است، یعنی فرم ارسال شده است
    if request.method == 'POST':
        form = ProductInstanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'محصول با موفقیت ثبت شد')
            return redirect('product_list')
    else:
        form = ProductInstanceForm()
    
    return render(request, 'core/product_list.html', {
        'products': products,
        'product_types': product_types,
        'form': form
    })

class ProductTypeListView(View):
    def get(self, request):
        product_types = ProductType.objects.all()
        return render(request, 'core/product_type_list.html', {
            'product_types': product_types
        })
