from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from typing import Dict, Any, Union

from .models import ProductType, ProductInstance, Category, Recipe, RecipeItem
from .forms import ProductForm, RecipeForm, RecipeItemForm


@login_required
def product_list(request) -> Union[redirect, render]:
    """
    View for listing and creating product instances.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
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
    """View for listing product types (staff only)."""
    model = ProductType
    template_name = 'core/product_type_list.html'
    context_object_name = 'product_types'


def get_product_type_unit(request) -> JsonResponse:
    """
    AJAX view to return the unit for a given product type.
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
def recipe_list(request) -> render:
    """
    View for displaying user's recipe list.
    """
    recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'recipes': recipes,
    }
    return render(request, 'core/recipe_list.html', context)


@login_required
def recipe_create(request) -> Union[redirect, render]:
    """
    View for creating a new recipe.
    """
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
def recipe_detail(request, recipe_id: int) -> Union[redirect, render]:
    """
    View for displaying recipe details and managing ingredients.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe_items = recipe.recipe_items.all()
    
    # Form for adding new ingredient
    if request.method == 'POST':
        form = RecipeItemForm(request.user, request.POST)
        if form.is_valid():
            recipe_item = form.save(commit=False)
            recipe_item.recipe = recipe
            recipe_item.save()
            
            # Update the total cost of the recipe
            recipe.calculate_total_cost()
            
            messages.success(request, "ماده اولیه با موفقیت اضافه شد.")
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeItemForm(request.user)
    
    # Calculate statistics
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
def recipe_item_delete(request, item_id: int) -> redirect:
    """
    View for deleting a recipe ingredient.
    """
    recipe_item = get_object_or_404(RecipeItem, id=item_id)
    recipe = recipe_item.recipe
    
    # Check ownership
    if recipe.user != request.user:
        messages.error(request, "شما اجازه حذف این ماده را ندارید.")
        return redirect('recipe_list')
    
    recipe_item.delete()
    
    # Update the total cost of the recipe
    recipe.calculate_total_cost()
    
    messages.success(request, "ماده اولیه با موفقیت حذف شد.")
    return redirect('recipe_detail', recipe_id=recipe.id)


@login_required
def recipe_update(request, recipe_id: int) -> Union[redirect, render]:
    """
    View for updating recipe information.
    """
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
def recipe_delete(request, recipe_id: int) -> Union[redirect, render]:
    """
    View for deleting a recipe.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, "دستور غذا با موفقیت حذف شد.")
        return redirect('recipe_list')
    
    context = {
        'recipe': recipe,
    }
    return render(request, 'core/recipe_delete.html', context)
