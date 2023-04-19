from django.contrib import admin
from .models import (
    Account,
    Budget,
    TransactionCategory,
    TransactionSubCategory,
    Transaction,
    ProductCategory,
    ProductSubCategory,
    Target,
    Employee,
    Product,
    TransactionType,
)

# Register your models here.


@admin.register(TransactionType)
class TransactionTypeAdminView(admin.ModelAdmin):
    model = TransactionType


@admin.register(TransactionCategory)
class TransactionCategoryAdminView(admin.ModelAdmin):
    model = TransactionCategory


@admin.register(TransactionSubCategory)
class TransactionSubCategoryAdminView(admin.ModelAdmin):
    model = TransactionSubCategory


@admin.register(ProductCategory)
class ProductCategoryAdminView(admin.ModelAdmin):
    model = ProductCategory


@admin.register(ProductSubCategory)
class ProductSubCategoryAdminView(admin.ModelAdmin):
    model = ProductSubCategory


@admin.register(Account)
class AccountAdminView(admin.ModelAdmin):
    model = Account

    list_display = (
        "account_name",
        "account_type",
    )

    list_filter = (
        "account_type",
        "created_at",
        "updated_at",
    )


@admin.register(Transaction)
class TransactionAdminView(admin.ModelAdmin):
    model = Transaction

    list_display = ("transaction_type",)

    list_filter = (
        "transaction_type",
        "created_at",
        "updated_at",
    )


@admin.register(Budget)
class BudgetAdminView(admin.ModelAdmin):
    model = Budget

    list_display = ("budget_name",)

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(Target)
class TargetAdminView(admin.ModelAdmin):
    model = Target

    list_display = ("target_name",)

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(Employee)
class EmployeeAdminView(admin.ModelAdmin):
    model = Employee

    list_display = (
        "first_name",
        "last_name",
    )

    list_filter = (
        "date_of_hire",
        "created_at",
        "updated_at",
    )


@admin.register(Product)
class ProductAdminView(admin.ModelAdmin):
    model = Target

    list_display = ("name",)

    list_filter = (
        "created_at",
        "updated_at",
    )
