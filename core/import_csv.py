import csv
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db_fa.settings')
django.setup()

from core.models import ProductType

def import_csv_data(csv_file_path):
    """
    Import product types from CSV file
    """
    # Delete all existing product types
    ProductType.objects.all().delete()
    
    # Import from CSV
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            try:
                # Check if row has a product type and it's not empty
                if 'نوع' in row and row['نوع'].strip():
                    # Convert empty strings to None or 0
                    base_weight = float(row['وزن پایه '].strip()) if row['وزن پایه '].strip() else 0
                    waste = float(row['دور ریز '].strip()) if row['دور ریز '].strip() else 0
                    
                    # Create the product type
                    ProductType.objects.create(
                        name=row['نوع'],
                        base_weight=base_weight,
                        waste=waste
                    )
                    print(f"نوع محصول ثبت شد: {row['نوع']}")
            except Exception as e:
                print(f"خطا در ثبت نوع محصول {row.get('نوع', 'نامشخص')}: {str(e)}")

if __name__ == "__main__":
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test.csv')
    import_csv_data(csv_file_path)
    print("عملیات وارد کردن انواع محصول به پایان رسید.") 