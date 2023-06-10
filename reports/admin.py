from django.contrib import admin
from reports.models import (
    CashFlowRecord,
    IncomeStatement,
    CashFlowStatement,
    BalanceSheetStatement,
    CashFlowStatementIdentifier,
)


@admin.register(CashFlowRecord)
class CashFlowRecordAdminView(admin.ModelAdmin):
    model = CashFlowRecord


@admin.register(CashFlowStatement)
class CashFlowStatementAdminView(admin.ModelAdmin):
    model = CashFlowStatement


@admin.register(CashFlowStatementIdentifier)
class CashFlowStatementIdentifierAdminView(admin.ModelAdmin):
    model = CashFlowStatementIdentifier


@admin.register(IncomeStatement)
class IncomeStatementAdminView(admin.ModelAdmin):
    model = IncomeStatement


@admin.register(BalanceSheetStatement)
class BalanceSheetStatementAdminView(admin.ModelAdmin):
    model = BalanceSheetStatement
