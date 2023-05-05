from plans.models import Plan
from django.contrib import admin


@admin.register(Plan)
class PlanAdminView(admin.ModelAdmin):
    model = Plan

    list_filter = (
        "created_at",
        "updated_at",
    )
