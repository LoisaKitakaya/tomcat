from django.contrib import admin
from reports.models import (
    BusinessActivity,
    CashFlowStatement,
    CashFlowItem,
    CashFlowRecord,
)


@admin.register(BusinessActivity)
class BusinessActivityAdminView(admin.ModelAdmin):
    model = BusinessActivity


@admin.register(CashFlowStatement)
class CashFlowStatementAdminView(admin.ModelAdmin):
    model = CashFlowStatement


@admin.register(CashFlowItem)
class CashFlowItemAdminView(admin.ModelAdmin):
    model = CashFlowItem


@admin.register(CashFlowRecord)
class CashFlowRecordAdminView(admin.ModelAdmin):
    model = CashFlowRecord
