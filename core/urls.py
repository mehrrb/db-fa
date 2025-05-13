from django.urls import path
from . import views
from .views import ProductTypeListView

urlpatterns = [
    # Product management URLs
    path('', views.product_list, name='product_list'),
    path('product-types/', ProductTypeListView.as_view(), name='product_type_list'),
    path('get-product-type-unit/', views.get_product_type_unit, name='get_product_type_unit'),
    
    # Recipe management URLs
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/new/', views.recipe_create, name='recipe_create'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:recipe_id>/edit/', views.recipe_update, name='recipe_update'),
    path('recipes/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    
    # Recipe item management URLs
    path('recipe-items/<int:item_id>/delete/', views.recipe_item_delete, name='recipe_item_delete'),
] 