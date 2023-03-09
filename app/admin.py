from django.contrib import admin
from .models import Account, Budget, Category, Report, Transaction

# Register your models here.

@admin.register(Account)
class AccountAdminView(admin.ModelAdmin):

    model = Account

    list_display = (
        'account_name',
        'account_type',
    )

    list_filter = (
        'account_type',
        'created_at',
        'updated_at',
    )

@admin.register(Budget)
class BudgetAdminView(admin.ModelAdmin):

    model = Budget

    list_display = (
        'budget_name',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )

@admin.register(Category)
class CategoryAdminView(admin.ModelAdmin):

    model = Category

@admin.register(Report)
class ReportAdminView(admin.ModelAdmin):

    model = Report

    list_filter = (
        'created_at',
        'updated_at',
    )

@admin.register(Transaction)
class TransactionAdminView(admin.ModelAdmin):

    model = Transaction

    list_display = (
        'transaction_type',
    )

    list_filter = (
        'transaction_type',
        'created_at',
        'updated_at',
    )