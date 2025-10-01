from typing import Union

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .forms import ProductForm, RecipeForm, RecipeItemForm
from .models import Category, ProductInstance, ProductType, Recipe, RecipeItem
from .serializers import (
    CategorySerializer,
    ProductInstanceSerializer,
    ProductTypeSerializer,
    RecipeItemSerializer,
    RecipeSerializer,
)

# API ViewSets


class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProductTypeViewSet(viewsets.ModelViewSet):
    """API endpoint for product types."""

    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    filterset_fields = ["category", "unit"]
    search_fields = ["name"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProductInstanceViewSet(viewsets.ModelViewSet):
    """API endpoint for product instances."""

    serializer_class = ProductInstanceSerializer
    filterset_fields = ["product_type", "unit"]
    search_fields = ["product_type__name"]

    def get_queryset(self):
        """Filter queryset by the current user."""
        if self.request.user.is_staff:
            return ProductInstance.objects.all()
        return ProductInstance.objects.filter(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    """API endpoint for recipes."""

    serializer_class = RecipeSerializer
    search_fields = ["name", "description"]

    def get_queryset(self):
        """Filter queryset by the current user."""
        if self.request.user.is_staff:
            return Recipe.objects.all()
        return Recipe.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"])
    def recalculate_cost(self, request, pk=None):
        """Endpoint for recalculating recipe cost."""
        recipe = self.get_object()
        total_cost = recipe.calculate_total_cost()
        return Response({"total_cost": total_cost})


class RecipeItemViewSet(viewsets.ModelViewSet):
    """API endpoint for recipe items."""

    serializer_class = RecipeItemSerializer

    def get_queryset(self):
        """Filter queryset by the current user's recipes."""
        if self.request.user.is_staff:
            return RecipeItem.objects.all()
        return RecipeItem.objects.filter(recipe__user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Override create to validate recipe ownership."""
        recipe_id = request.data.get("recipe")
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            if recipe.user != request.user and not request.user.is_staff:
                return Response(
                    {
                        "detail": "You do not have permission to add items to this recipe."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Recipe.DoesNotExist:
            return Response(
                {"detail": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND
            )

        response = super().create(request, *args, **kwargs)

        # Recalculate recipe cost
        if response.status_code == status.HTTP_201_CREATED:
            recipe.calculate_total_cost()

        return response

    def destroy(self, request, *args, **kwargs):
        """Override destroy to recalculate recipe cost after deletion."""
        instance = self.get_object()
        recipe = instance.recipe

        response = super().destroy(request, *args, **kwargs)

        # Recalculate recipe cost
        if response.status_code == status.HTTP_204_NO_CONTENT:
            recipe.calculate_total_cost()

        return response


# Legacy views for template-based access


@login_required
def product_list(request) -> Union[redirect, render]:
    """
    View for listing and creating product instances.
    """
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect("product_list")
    else:
        form = ProductForm()

    # Filter products by the current user
    products = ProductInstance.objects.filter(user=request.user).order_by("-created_at")

    # Get all product types for JavaScript unit mapping
    product_types = ProductType.objects.all()

    context = {
        "form": form,
        "products": products,
        "product_types": product_types,
    }
    return render(request, "core/product_list.html", context)


@method_decorator(staff_member_required, name="dispatch")
class ProductTypeListView(ListView):
    """View for listing product types (staff only)."""

    model = ProductType
    template_name = "core/product_type_list.html"
    context_object_name = "product_types"


def get_product_type_unit(request) -> JsonResponse:
    """
    AJAX view to return the unit for a given product type.
    """
    product_type_id = request.GET.get("id")
    if not product_type_id:
        return JsonResponse({"error": "No product type ID provided"}, status=400)

    try:
        product_type = ProductType.objects.get(id=product_type_id)
        return JsonResponse({"unit": product_type.unit})
    except ProductType.DoesNotExist:
        return JsonResponse({"error": "Product type not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def recipe_list(request) -> render:
    """
    View for displaying user's recipe list.
    """
    recipes = Recipe.objects.filter(user=request.user).order_by("-created_at")

    context = {
        "recipes": recipes,
    }
    return render(request, "core/recipe_list.html", context)


@login_required
def recipe_create(request) -> Union[redirect, render]:
    """
    View for creating a new recipe.
    """
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            messages.success(request, "دستور غذای جدید با موفقیت ایجاد شد.")
            return redirect("recipe_detail", recipe_id=recipe.id)
    else:
        form = RecipeForm()

    context = {
        "form": form,
    }
    return render(request, "core/recipe_form.html", context)


@login_required
def recipe_detail(request, recipe_id: int) -> Union[redirect, render]:
    """
    View for displaying recipe details and managing ingredients.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe_items = recipe.recipe_items.all()

    # Form for adding new ingredient
    if request.method == "POST":
        form = RecipeItemForm(request.user, request.POST)
        if form.is_valid():
            recipe_item = form.save(commit=False)
            recipe_item.recipe = recipe
            recipe_item.save()

            # Update the total cost of the recipe
            recipe.calculate_total_cost()

            messages.success(request, "ماده اولیه با موفقیت اضافه شد.")
            return redirect("recipe_detail", recipe_id=recipe.id)
    else:
        form = RecipeItemForm(request.user)

    # Calculate statistics
    profit = recipe.calculate_profit()
    profit_percentage = recipe.calculate_profit_percentage()

    context = {
        "recipe": recipe,
        "recipe_items": recipe_items,
        "form": form,
        "profit": profit,
        "profit_percentage": profit_percentage,
    }
    return render(request, "core/recipe_detail.html", context)


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
        return redirect("recipe_list")

    recipe_item.delete()

    # Update the total cost of the recipe
    recipe.calculate_total_cost()

    messages.success(request, "ماده اولیه با موفقیت حذف شد.")
    return redirect("recipe_detail", recipe_id=recipe.id)


@login_required
def recipe_update(request, recipe_id: int) -> Union[redirect, render]:
    """
    View for updating recipe information.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "دستور غذا با موفقیت به‌روزرسانی شد.")
            return redirect("recipe_detail", recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    context = {
        "form": form,
        "recipe": recipe,
    }
    return render(request, "core/recipe_form.html", context)


@login_required
def recipe_delete(request, recipe_id: int) -> Union[redirect, render]:
    """
    View for deleting a recipe.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)

    if request.method == "POST":
        recipe.delete()
        messages.success(request, "دستور غذا با موفقیت حذف شد.")
        return redirect("recipe_list")

    context = {
        "recipe": recipe,
    }
    return render(request, "core/recipe_confirm_delete.html", context)
