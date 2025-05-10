from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """مدل برای دسته‌بندی انواع محصولات"""
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

class ProductType(models.Model):
    """مدل برای نگهداری انواع محصولات با مقادیر ثابت"""
    # انواع واحدهای اندازه‌گیری
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_types', null=True, blank=True, verbose_name="دسته‌بندی")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=UNIT_GRAM, verbose_name="واحد")
    
    # نسبت دور ریز به وزن پایه
    @property
    def waste_ratio(self):
        if self.base_weight > 0:
            return self.waste / self.base_weight
        return 0
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "نوع محصول"
        verbose_name_plural = "انواع محصولات"

class ProductInstance(models.Model):
    """نمونه محصول با قیمت و مقادیر محاسبه شده"""
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name="نوع محصول")
    total_weight = models.FloatField(default=1000, verbose_name="مقدار")
    price_per_kilo = models.FloatField(default=10000, verbose_name="قیمت هر واحد")
    
    # افزودن فیلد واحد - کاربر می‌تواند واحد را خودش انتخاب کند
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
    
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=UNIT_GRAM, verbose_name="واحد")
    
    # مقادیر محاسبه شده
    waste_weight = models.FloatField(null=True, blank=True, verbose_name="وزن دور ریز")
    net_weight = models.FloatField(null=True, blank=True, verbose_name="وزن خالص")
    total_price = models.FloatField(null=True, blank=True, verbose_name="قیمت کل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='کاربر', null=True)
    
    def save(self, *args, **kwargs):
        # محاسبه وزن دور ریز بر اساس نسبت دور ریز نوع محصول
        waste_ratio = self.product_type.waste_ratio
        self.waste_weight = self.total_weight * waste_ratio
        
        # محاسبه وزن خالص
        self.net_weight = self.total_weight - self.waste_weight
        
        # محاسبه قیمت کل با در نظر گرفتن دور ریز
        # محاسبه قیمت بر اساس وزن کل
        self.total_price = (self.price_per_kilo * self.total_weight) / 1000
        
        # قیمت اضافی بابت دور ریز
        # این بخش باعث می‌شود قیمت کل با توجه به دور ریز افزایش یابد
        waste_cost = (self.price_per_kilo * self.waste_weight) / 1000
        self.total_price += waste_cost
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product_type.name} - {self.total_weight} گرم - {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
