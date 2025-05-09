from django.db import models

# Create your models here.
class ProductType(models.Model):
    """مدل برای نگهداری انواع محصولات با مقادیر ثابت"""
    name = models.CharField(max_length=100, verbose_name="نوع محصول")
    base_weight = models.FloatField(verbose_name="وزن پایه")
    waste = models.FloatField(verbose_name="دور ریز")
    
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
    total_weight = models.FloatField(default=1000, verbose_name="وزن کل (گرم)")
    price_per_kilo = models.FloatField(default=10000, verbose_name="قیمت هر کیلو")
    
    # مقادیر محاسبه شده
    waste_weight = models.FloatField(null=True, blank=True, verbose_name="وزن دور ریز")
    net_weight = models.FloatField(null=True, blank=True, verbose_name="وزن خالص")
    total_price = models.FloatField(null=True, blank=True, verbose_name="قیمت کل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    def save(self, *args, **kwargs):
        # محاسبه وزن دور ریز بر اساس نسبت دور ریز نوع محصول
        waste_ratio = self.product_type.waste_ratio
        self.waste_weight = self.total_weight * waste_ratio
        
        # محاسبه وزن خالص
        self.net_weight = self.total_weight - self.waste_weight
        
        # محاسبه قیمت کل (قیمت هر کیلو * وزن کل به کیلوگرم)
        self.total_price = (self.price_per_kilo * self.total_weight) / 1000  # تبدیل گرم به کیلوگرم
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product_type.name} - {self.total_weight} گرم - {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
