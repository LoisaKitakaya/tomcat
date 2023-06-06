from django.db import models
from accounts.models import Account


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100, blank=False, unique=True)
    category_description = models.TextField(blank=False)

    class Meta:
        verbose_name = "product category"
        verbose_name_plural = "product categories"
        db_table = "ProductCategories"

    def __str__(self) -> str:
        return self.category_name


class ProductSubCategory(models.Model):
    parent = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100, blank=False, unique=True)
    category_description = models.TextField(blank=False)

    class Meta:
        verbose_name = "product sub category"
        verbose_name_plural = "product sub categories"
        db_table = "ProductSubCategories"

    def __str__(self) -> str:
        return self.category_name


class Product(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE)
    buying_price = models.FloatField(default=0.0, blank=False)
    selling_price = models.FloatField(default=0.0, blank=False)
    current_stock_level = models.IntegerField(default=0, blank=False)
    units_sold = models.IntegerField(default=0, blank=False)
    profit_generated = models.FloatField(default=0.0, blank=True)
    supplier_name = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "product"
        verbose_name_plural = "products"
        db_table = "Products"

    def __str__(self) -> str:
        return self.name
