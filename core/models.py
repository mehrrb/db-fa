from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from typing import Optional, Union

# Create your models here.
class Category(models.Model):
    """Category model for classifying different product types."""
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

class ProductType(models.Model):
    """Model for storing product types with fixed values."""
    # Measurement unit constants
    UNIT_GRAM = 'gram'
    UNIT_PIECE = 'piece'
    UNIT_LITER = 'liter'
    UNIT_METER = 'meter'
    
    UNIT_CHOICES = [
        (UNIT_GRAM, 'گرم'),
        (UNIT_PIECE, 'عدد'),
        (UNIT_LITER, 'لیتر'),
        (UNIT_METER, 'متر'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="نوع محصول")
    base_weight = models.FloatField(verbose_name="وزن پایه")
    waste = models.FloatField(verbose_name="دور ریز")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='product_types', 
        null=True, 
        blank=True, 
        verbose_name="دسته‌بندی"
    )
    unit = models.CharField(
        max_length=10, 
        choices=UNIT_CHOICES, 
        default=UNIT_GRAM, 
        verbose_name="واحد"
    )
    
    @property
    def waste_ratio(self) -> float:
        """Calculate waste to base weight ratio."""
        if self.base_weight > 0:
            return self.waste / self.base_weight
        return 0
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "نوع محصول"
        verbose_name_plural = "انواع محصولات"

class ProductInstance(models.Model):
    """Product instance with price and calculated values."""
    # Measurement unit constants - same as ProductType
    UNIT_GRAM = 'gram'
    UNIT_PIECE = 'piece'
    UNIT_LITER = 'liter'
    UNIT_METER = 'meter'
    
    UNIT_CHOICES = [
        (UNIT_GRAM, 'گرم'),
        (UNIT_PIECE, 'عدد'),
        (UNIT_LITER, 'لیتر'),
        (UNIT_METER, 'متر'),
    ]
    
    product_type = models.ForeignKey(
        ProductType, 
        on_delete=models.CASCADE, 
        verbose_name="نوع محصول"
    )
    total_weight = models.FloatField(
        default=1000, 
        verbose_name="مقدار"
    )
    price_per_kilo = models.FloatField(
        default=10000, 
        verbose_name="قیمت هر واحد"
    )
    unit = models.CharField(
        max_length=10, 
        choices=UNIT_CHOICES, 
        default=UNIT_GRAM, 
        verbose_name="واحد"
    )
    
    # Calculated values
    waste_weight = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="وزن دور ریز"
    )
    net_weight = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="وزن خالص"
    )
    total_price = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="قیمت کل"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="تاریخ ایجاد"
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='products', 
        verbose_name='کاربر', 
        null=True
    )
    
    def save(self, *args, **kwargs) -> None:
        """Calculate waste weight, net weight and total price before saving."""
        # Calculate waste weight based on product type waste ratio
        waste_ratio = self.product_type.waste_ratio
        self.waste_weight = self.total_weight * waste_ratio
        
        # Calculate net weight
        self.net_weight = self.total_weight - self.waste_weight
        
        # Calculate total price considering waste
        # Price based on total weight
        self.total_price = (self.price_per_kilo * self.total_weight) / 1000
        
        # Additional cost for waste
        waste_cost = (self.price_per_kilo * self.waste_weight) / 1000
        self.total_price += waste_cost
            
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.product_type.name} - {self.total_weight} گرم - {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

class Recipe(models.Model):
    """Model for storing recipes and calculating costs."""
    name = models.CharField(max_length=200, verbose_name="نام غذا")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='recipes', 
        verbose_name='کاربر'
    )
    
    # Calculated final price
    total_cost = models.FloatField(default=0, verbose_name="هزینه کل")
    selling_price = models.FloatField(blank=True, null=True, verbose_name="قیمت فروش")
    
    def calculate_total_cost(self) -> float:
        """Calculate total cost based on ingredients."""
        total = 0
        for item in self.recipe_items.all():
            # Calculate price of each ingredient based on quantity and price
            if item.product_instance.unit == ProductType.UNIT_GRAM:
                # For weight-based items (grams)
                item_cost = (item.product_instance.price_per_kilo * item.quantity) / 1000
            else:
                # For other units (piece, liter, meter)
                item_cost = item.product_instance.price_per_kilo * item.quantity
                
            total += item_cost
            
        self.total_cost = total
        self.save()
        return total
    
    def calculate_profit(self) -> float:
        """Calculate net profit."""
        if not self.selling_price:
            return 0
        return self.selling_price - self.total_cost
    
    def calculate_profit_percentage(self) -> float:
        """Calculate profit percentage."""
        if not self.selling_price or self.total_cost == 0:
            return 0
        return (self.selling_price - self.total_cost) / self.total_cost * 100
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "دستور غذا"
        verbose_name_plural = "دستورهای غذا"

class RecipeItem(models.Model):
    """Model for storing ingredients of a recipe."""
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE, 
        related_name='recipe_items', 
        verbose_name="دستور غذا"
    )
    product_instance = models.ForeignKey(
        ProductInstance, 
        on_delete=models.CASCADE, 
        verbose_name="ماده اولیه"
    )
    quantity = models.FloatField(default=1, verbose_name="مقدار")
    
    def __str__(self) -> str:
        unit_display = {
            'gram': 'گرم',
            'piece': 'عدد',
            'liter': 'لیتر',
            'meter': 'متر'
        }.get(self.product_instance.unit, 'واحد')
        
        return f"{self.quantity} {unit_display} {self.product_instance.product_type.name}"
    
    class Meta:
        verbose_name = "ماده تشکیل‌دهنده"
        verbose_name_plural = "مواد تشکیل‌دهنده"
