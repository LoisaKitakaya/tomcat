from django.contrib import admin
from billing.models import PlanBilling, Plan


# Register your models here.
@admin.register(PlanBilling)
class PlanBillingAdminView(admin.ModelAdmin):
    model = PlanBilling

    list_display = ("merchant_ref",)

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(Plan)
class PlanAdminView(admin.ModelAdmin):
    model = Plan

    list_filter = (
        "created_at",
        "updated_at",
    )
