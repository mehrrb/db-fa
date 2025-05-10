from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('types/', views.ProductTypeListView.as_view(), name='product_type_list'),
] 