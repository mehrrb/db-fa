from django.contrib import admin
from .models import ProductType, ProductInstance

# Register your models here.
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_weight', 'waste')
    search_fields = ('name',)

@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'total_weight', 'waste_weight', 'net_weight', 'price_per_kilo', 'total_price', 'created_at')
    list_filter = ('product_type', 'created_at')
    readonly_fields = ('waste_weight', 'net_weight', 'total_price')
    autocomplete_fields = ('product_type',)
