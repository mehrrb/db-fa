import csv
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db_fa.settings')
django.setup()

from core.models import Product

def import_csv_data(csv_file_path):
    """
    Import data from CSV file to Product model
    """
    # Delete all existing products
    Product.objects.all().delete()
    
    # Import from CSV
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            try:
                # Convert empty strings to None
                base_weight = float(row['وزن پایه ']) if row['وزن پایه '].strip() else None
                waste = float(row['دور ریز ']) if row['دور ریز '].strip() else None
                net_weight = float(row['وزن خالص']) if row['وزن خالص'].strip() else None
                base_price = float(row['قیمت محصول بر پایه وزن پایه ']) if row['قیمت محصول بر پایه وزن پایه '].strip() else None
                real_price = float(row['قیمت حقیقی ']) if row['قیمت حقیقی '].strip() else None
                
                Product.objects.create(
                    product_type=row['نوع'],
                    base_weight=base_weight,
                    waste=waste,
                    net_weight=net_weight,
                    base_price=base_price,
                    real_price=real_price
                )
                print(f"ثبت محصول: {row['نوع']}")
            except Exception as e:
                print(f"خطا در ثبت محصول {row['نوع']}: {str(e)}")

if __name__ == "__main__":
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test.csv')
    import_csv_data(csv_file_path)
    print("عملیات وارد کردن داده‌ها به پایان رسید.") 