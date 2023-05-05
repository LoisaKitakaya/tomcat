from django.contrib import admin
from budgets.models import Budget


@admin.register(Budget)
class BudgetAdminView(admin.ModelAdmin):
    model = Budget

    list_display = ("budget_name",)

    list_filter = (
        "created_at",
        "updated_at",
    )
