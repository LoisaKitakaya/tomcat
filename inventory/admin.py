from django.contrib import admin
from inventory.models import Product, ProductCategory, ProductSubCategory

# Register your models here.


@admin.register(ProductCategory)
class ProductCategoryAdminView(admin.ModelAdmin):
    model = ProductCategory


@admin.register(ProductSubCategory)
class ProductSubCategoryAdminView(admin.ModelAdmin):
    model = ProductSubCategory


@admin.register(Product)
class ProductAdminView(admin.ModelAdmin):
    model = Product

    list_display = ("name",)

    list_filter = (
        "created_at",
        "updated_at",
    )
