from django.contrib import admin
from billing.models import PlanBilling


# Register your models here.
@admin.register(PlanBilling)
class PlanBillingAdminView(admin.ModelAdmin):
    model = PlanBilling

    list_display = ("merchant_ref",)

    list_filter = (
        "created_at",
        "updated_at",
    )
