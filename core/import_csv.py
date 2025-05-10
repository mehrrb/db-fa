import csv
import os
import sys
import django

# Add the project directory to the Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db_fa.settings')
django.setup()

from core.models import ProductType, Category

def import_csv_data(csv_file_path):
    """
    Import product types from CSV file
    """
    # Import from CSV
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        # Skip header row
        next(csv_reader)
        
        current_category = None
        
        for row in csv_reader:
            if not row or len(row) < 3:
                continue
                
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
                        print(f"Category {'created' if created else 'retrieved'}: {product_name}")
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
                                print(f"Product type updated: {product_name}")
                            except ProductType.DoesNotExist:
                                ProductType.objects.create(
                                    name=product_name,
                                    base_weight=base_weight,
                                    waste=waste,
                                    category=current_category
                                )
                                print(f"Product type created: {product_name}")
                        except ValueError as e:
                            print(f"Error converting numeric values for product {product_name}: {str(e)}")
            except Exception as e:
                print(f"Error processing row {row}: {str(e)}")

if __name__ == "__main__":
    csv_file_path = os.path.join(BASE_DIR, 'test.csv')
    print(f"Starting import from file: {csv_file_path}")
    import_csv_data(csv_file_path)
    print("Product type import operation completed.")