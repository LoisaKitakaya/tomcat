from django.contrib import admin
from transactions.models import (
    Transaction,
    TransactionType,
    TransactionCategory,
    TransactionSubCategory,
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


@admin.register(Transaction)
class TransactionAdminView(admin.ModelAdmin):
    model = Transaction

    list_display = ("transaction_type",)

    list_filter = (
        "transaction_type",
        "created_at",
        "updated_at",
    )
