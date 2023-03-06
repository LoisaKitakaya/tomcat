from django.contrib import admin
from .models import Account, Budget, BudgetCategory, Category, Report, ReportCategory, Transaction, TransactionCategory

# Register your models here.

@admin.register(Account)
class AccountAdminView(admin.ModelAdmin):

    model = Account

    list_display = (
        'account_name',
        'public_id',
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
        'public_id',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )

@admin.register(BudgetCategory)
class BudgetCategoryAdminView(admin.ModelAdmin):

    model = BudgetCategory

@admin.register(Category)
class CategoryAdminView(admin.ModelAdmin):

    model = Category

@admin.register(Report)
class ReportAdminView(admin.ModelAdmin):

    model = Report

    list_display = (
        'report_name',
        'public_id',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )

@admin.register(ReportCategory)
class ReportCategoryAdminView(admin.ModelAdmin):

    model = ReportCategory

@admin.register(Transaction)
class TransactionAdminView(admin.ModelAdmin):

    model = Transaction

    list_display = (
        'public_id',
        'transaction_type',
    )

    list_filter = (
        'transaction_type',
        'created_at',
        'updated_at',
    )

@admin.register(TransactionCategory)
class TransactionCategoryAdminView(admin.ModelAdmin):

    model = TransactionCategory