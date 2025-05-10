from django.urls import path
from . import views
from .views import ProductTypeListView

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product-types/', ProductTypeListView.as_view(), name='product_type_list'),
    path('get-product-type-unit/', views.get_product_type_unit, name='get_product_type_unit'),
] 