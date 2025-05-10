from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
import csv
import io
from .models import ProductType, ProductInstance, Category

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_weight', 'waste', 'waste_ratio')
    list_filter = ('category',)
    search_fields = ('name',)
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-csv/', self.import_csv, name='import_csv'),
        ]
        return new_urls + urls
    
    def import_csv(self, request):
        if request.method == "POST":
            csv_form = CsvImportForm(request.POST, request.FILES)
            if csv_form.is_valid():
                csv_file = request.FILES["csv_file"]
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                next(io_string)  # Skip header row
                
                for line in csv.reader(io_string, delimiter=','):
                    if len(line) < 3:  # Skip empty or incomplete lines
                        continue
                        
                    # Check if this is a category line or a product line
                    if line[1].strip() == '' and line[2].strip() == '':
                        # This is a category line
                        category_name = line[0].strip()
                        if category_name:
                            category, created = Category.objects.get_or_create(name=category_name)
                            current_category = category
                        else:
                            current_category = None
                    else:
                        # This is a product line
                        product_name = line[0].strip()
                        try:
                            base_weight = float(line[1].strip())
                            waste = float(line[2].strip())
                            
                            # Check if product already exists
                            try:
                                product = ProductType.objects.get(name=product_name)
                                product.base_weight = base_weight
                                product.waste = waste
                                if 'current_category' in locals():
                                    product.category = current_category
                                product.save()
                            except ProductType.DoesNotExist:
                                ProductType.objects.create(
                                    name=product_name,
                                    base_weight=base_weight,
                                    waste=waste,
                                    category=current_category if 'current_category' in locals() else None
                                )
                        except (ValueError, IndexError):
                            messages.error(request, f"Error with line: {line}")
                
                messages.success(request, "مقادیر ثابت محصولات با موفقیت وارد شدند")
                return redirect("admin:core_producttype_changelist")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            csv_form = CsvImportForm()
            
        return render(
            request,
            "admin/csv_import.html",
            {"form": csv_form}
        )


@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product_type', 'total_weight', 'waste_weight', 'net_weight', 'price_per_kilo', 'total_price', 'created_at')
    list_filter = ('product_type__category', 'product_type')
    search_fields = ('product_type__name',)
    date_hierarchy = 'created_at'
