from django.contrib import admin
from invoice.models import PaymentAccount, ClientInformation, Invoice


@admin.register(PaymentAccount)
class PaymentAccountAdminView(admin.ModelAdmin):
    model = PaymentAccount


@admin.register(ClientInformation)
class ClientInformationAdminView(admin.ModelAdmin):
    model = ClientInformation


@admin.register(Invoice)
class InvoiceAdminView(admin.ModelAdmin):
    model = Invoice

    list_filter = (
        "due_date",
        "created_at",
        "updated_at",
    )
