from django.contrib import admin
from debts.models import Customer, Debt


@admin.register(Customer)
class CustomerAdminView(admin.ModelAdmin):
    model = Customer

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(Debt)
class DebtAdminView(admin.ModelAdmin):
    model = Debt

    list_filter = (
        "created_at",
        "updated_at",
    )
