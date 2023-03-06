from django.contrib import admin
from .models import Account, Budget, BudgetCategory, Category, Report, ReportCategory, ReportTransaction, ReportAccount, Transaction, TransactionCategory

# Register your models here.

@admin.register(Account)
class AccountAdminView(admin.ModelAdmin):

    model = Account

@admin.register(Budget)
class BudgetAdminView(admin.ModelAdmin):

    model = Budget

@admin.register(BudgetCategory)
class BudgetCategoryAdminView(admin.ModelAdmin):

    model = BudgetCategory

@admin.register(Category)
class CategoryAdminView(admin.ModelAdmin):

    model = Category

@admin.register(Report)
class ReportAdminView(admin.ModelAdmin):

    model = Report

@admin.register(ReportCategory)
class ReportCategoryAdminView(admin.ModelAdmin):

    model = ReportCategory

@admin.register(ReportTransaction)
class ReportTransactionAdminView(admin.ModelAdmin):

    model = ReportTransaction

@admin.register(ReportAccount)
class ReportAccountAdminView(admin.ModelAdmin):

    model = ReportAccount

@admin.register(Transaction)
class TransactionAdminView(admin.ModelAdmin):

    model = Transaction

@admin.register(TransactionCategory)
class TransactionCategoryAdminView(admin.ModelAdmin):

    model = TransactionCategory