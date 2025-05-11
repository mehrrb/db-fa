from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from .models import ProductType, ProductInstance, Category, Recipe, RecipeItem
from .forms import ProductForm, RecipeForm, RecipeItemForm
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

@method_decorator(staff_member_required, name='dispatch')
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

@login_required
def recipe_list(request):
    """نمایش لیست دستورات غذایی کاربر"""
    recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'recipes': recipes,
    }
    return render(request, 'core/recipe_list.html', context)

@login_required
def recipe_create(request):
    """ایجاد دستور غذای جدید"""
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            messages.success(request, "دستور غذای جدید با موفقیت ایجاد شد.")
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
        
    context = {
        'form': form,
    }
    return render(request, 'core/recipe_form.html', context)

@login_required
def recipe_detail(request, recipe_id):
    """نمایش جزئیات دستور غذا و مواد تشکیل‌دهنده آن"""
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe_items = recipe.recipe_items.all()
    
    # فرم اضافه کردن ماده تشکیل‌دهنده جدید
    if request.method == 'POST':
        form = RecipeItemForm(request.user, request.POST)
        if form.is_valid():
            recipe_item = form.save(commit=False)
            recipe_item.recipe = recipe
            recipe_item.save()
            
            # به‌روزرسانی قیمت کل دستور غذا
            recipe.calculate_total_cost()
            
            messages.success(request, "ماده اولیه با موفقیت اضافه شد.")
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeItemForm(request.user)
    
    # محاسبه آمارها
    profit = recipe.calculate_profit()
    profit_percentage = recipe.calculate_profit_percentage()
    
    context = {
        'recipe': recipe,
        'recipe_items': recipe_items,
        'form': form,
        'profit': profit,
        'profit_percentage': profit_percentage,
    }
    return render(request, 'core/recipe_detail.html', context)

@login_required
def recipe_item_delete(request, item_id):
    """حذف ماده تشکیل‌دهنده از دستور غذا"""
    recipe_item = get_object_or_404(RecipeItem, id=item_id)
    recipe = recipe_item.recipe
    
    # بررسی مالکیت
    if recipe.user != request.user:
        messages.error(request, "شما اجازه حذف این ماده را ندارید.")
        return redirect('recipe_list')
    
    recipe_item.delete()
    
    # به‌روزرسانی قیمت کل دستور غذا
    recipe.calculate_total_cost()
    
    messages.success(request, "ماده اولیه با موفقیت حذف شد.")
    return redirect('recipe_detail', recipe_id=recipe.id)

@login_required
def recipe_update(request, recipe_id):
    """ویرایش اطلاعات دستور غذا"""
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "دستور غذا با موفقیت به‌روزرسانی شد.")
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    
    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'core/recipe_form.html', context)

@login_required
def recipe_delete(request, recipe_id):
    """حذف دستور غذا"""
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, "دستور غذا با موفقیت حذف شد.")
        return redirect('recipe_list')
    
    context = {
        'recipe': recipe,
    }
    return render(request, 'core/recipe_confirm_delete.html', context)
