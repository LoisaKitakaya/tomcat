from django.contrib import admin
from billing.models import (
    CardPaymentMethod,
    CardBilling,
    MpesaPaymentMethod,
    MpesaBilling,
)

# Register your models here.
@admin.register(CardPaymentMethod)
class CardPaymentMethodAdminView(admin.ModelAdmin):

    model = CardPaymentMethod

    list_display = ("cardholder_name",)

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(CardBilling)
class CardBillingAdminView(admin.ModelAdmin):

    model = CardBilling

    list_display = ("transaction_uid",)

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(MpesaPaymentMethod)
class MpesaPaymentMethodAdminView(admin.ModelAdmin):

    model = MpesaPaymentMethod

    list_display = ("phone_owner",)

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(MpesaBilling)
class MpesaBillingAdminView(admin.ModelAdmin):

    model = MpesaBilling

    list_display = ("transaction_uid",)

    list_filter = (
        "created_at",
        "updated_at",
    )
