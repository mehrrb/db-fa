import csv
import os
from django.core.management.base import BaseCommand, CommandError
from core.models import ProductType, Category

class Command(BaseCommand):
    help = 'Import product types from CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='?', type=str, help='Path to the CSV file')
        
    def handle(self, *args, **options):
        # Get CSV file path
        csv_file_path = options.get('csv_file')
        
        # If no file path provided, use the default test.csv in project root
        if not csv_file_path:
            csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'test.csv')
        
        # Check if file exists
        if not os.path.exists(csv_file_path):
            raise CommandError(f"فایل CSV در مسیر {csv_file_path} یافت نشد.")
            
        # Import from CSV
        self.stdout.write(self.style.SUCCESS(f"شروع واردات از فایل: {csv_file_path}"))
        
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            # Skip header row
            next(csv_reader)
            
            current_category = None
            rows_processed = 0
            products_added = 0
            products_updated = 0
            categories_added = 0
            
            for row in csv_reader:
                if not row or len(row) < 3:
                    continue
                    
                rows_processed += 1
                product_name = row[0].strip()
                base_weight_str = row[1].strip() if len(row) > 1 else ""
                waste_str = row[2].strip() if len(row) > 2 else ""
                
                try:
                    # Check if this is a category row (no values in other columns)
                    if base_weight_str == "" and waste_str == "":
                        # This is a category
                        if product_name:
                            category, created = Category.objects.get_or_create(name=product_name)
                            current_category = category
                            if created:
                                categories_added += 1
                            self.stdout.write(f"دسته‌بندی {'ایجاد' if created else 'دریافت'} شد: {product_name}")
                    else:
                        # This is a product
                        if product_name:
                            try:
                                base_weight = float(base_weight_str) if base_weight_str else 0
                                waste = float(waste_str) if waste_str else 0
                                
                                # Check if product already exists
                                try:
                                    product = ProductType.objects.get(name=product_name)
                                    product.base_weight = base_weight
                                    product.waste = waste
                                    if current_category:
                                        product.category = current_category
                                    product.save()
                                    products_updated += 1
                                    self.stdout.write(f"نوع محصول به‌روزرسانی شد: {product_name}")
                                except ProductType.DoesNotExist:
                                    ProductType.objects.create(
                                        name=product_name,
                                        base_weight=base_weight,
                                        waste=waste,
                                        category=current_category
                                    )
                                    products_added += 1
                                    self.stdout.write(f"نوع محصول ایجاد شد: {product_name}")
                            except ValueError as e:
                                self.stdout.write(self.style.ERROR(f"خطا در تبدیل مقادیر عددی برای محصول {product_name}: {str(e)}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"خطا در پردازش سطر {row}: {str(e)}"))
            
            self.stdout.write(self.style.SUCCESS(f"""
عملیات وارد کردن انواع محصول به پایان رسید.
تعداد سطرهای پردازش شده: {rows_processed}
تعداد دسته‌بندی‌های جدید: {categories_added}
تعداد محصولات جدید: {products_added}
تعداد محصولات به‌روزرسانی شده: {products_updated}
""")) 