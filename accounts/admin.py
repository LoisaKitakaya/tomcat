from django.contrib import admin
from accounts.models import Account


@admin.register(Account)
class AccountAdminView(admin.ModelAdmin):
    model = Account

    list_display = (
        "account_name",
        "account_type",
    )

    list_filter = (
        "account_type",
        "created_at",
        "updated_at",
    )
