from django.db import models

# Create your models here.
class Product(models.Model):
    product_type = models.CharField(max_length=100, verbose_name="نوع")
    base_weight = models.FloatField(null=True, blank=True, verbose_name="وزن پایه")
    waste = models.FloatField(null=True, blank=True, verbose_name="دور ریز")
    net_weight = models.FloatField(null=True, blank=True, verbose_name="وزن خالص")
    base_price = models.FloatField(null=True, blank=True, verbose_name="قیمت محصول بر پایه وزن پایه")
    real_price = models.FloatField(null=True, blank=True, verbose_name="قیمت حقیقی")
    
    def __str__(self):
        return self.product_type
