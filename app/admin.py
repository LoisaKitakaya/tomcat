from django.contrib import admin
from .models import Account, Budget, Category, Transaction, Target, Employee, Product

# Register your models here.


@admin.register(Category)
class CategoryAdminView(admin.ModelAdmin):
    model = Category


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