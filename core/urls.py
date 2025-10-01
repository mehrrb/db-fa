from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import ProductTypeListView

# Create a router for DRF ViewSets
router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"product-types", views.ProductTypeViewSet)
router.register(r"products", views.ProductInstanceViewSet, basename="product")
router.register(r"recipes", views.RecipeViewSet, basename="recipe")
router.register(r"recipe-items", views.RecipeItemViewSet, basename="recipe-item")

urlpatterns = [
    # API URLs
    path("", include(router.urls)),
    # Legacy template-based URLs
    path("legacy/", views.product_list, name="product_list"),
    path(
        "legacy/product-types/", ProductTypeListView.as_view(), name="product_type_list"
    ),
    path(
        "legacy/get-product-type-unit/",
        views.get_product_type_unit,
        name="get_product_type_unit",
    ),
    # Recipe management legacy URLs
    path("legacy/recipes/", views.recipe_list, name="recipe_list"),
    path("legacy/recipes/new/", views.recipe_create, name="recipe_create"),
    path("legacy/recipes/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path(
        "legacy/recipes/<int:recipe_id>/edit/",
        views.recipe_update,
        name="recipe_update",
    ),
    path(
        "legacy/recipes/<int:recipe_id>/delete/",
        views.recipe_delete,
        name="recipe_delete",
    ),
    # Recipe item management legacy URLs
    path(
        "legacy/recipe-items/<int:item_id>/delete/",
        views.recipe_item_delete,
        name="recipe_item_delete",
    ),
]
