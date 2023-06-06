from django.db import models
from transactions.models import TransactionCategory, TransactionSubCategory


class PaymentAccount(models.Model):
    business_name = models.CharField(max_length=50, blank=False)
    business_email = models.EmailField(blank=False)
    business_phone_number = models.CharField(max_length=20, blank=False)
    bank_name = models.CharField(max_length=50, blank=False)
    bank_account = models.CharField(max_length=100, blank=False)
    mobile_payment_name = models.CharField(max_length=50, blank=False)
    mobile_account = models.CharField(max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "payment account"
        verbose_name_plural = "payment accounts"
        db_table = "PaymentAccounts"

    def __str__(self) -> str:
        return self.business_name


class ClientInformation(models.Model):
    client_name = models.CharField(max_length=50, blank=False)
    client_email = models.EmailField(blank=False)
    client_phone_number = models.CharField(max_length=20, blank=False)
    client_address = models.CharField(max_length=120, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "client information"
        verbose_name_plural = "clients information"
        db_table = "ClientsInformation"

    def __str__(self) -> str:
        return self.client_name


class Invoice(models.Model):
    business = models.ForeignKey(PaymentAccount, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientInformation, on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(TransactionSubCategory, on_delete=models.CASCADE)
    item = models.CharField(max_length=100, blank=False)
    quantity = models.IntegerField(default=0, blank=False)
    amount = models.FloatField(default=0.0, blank=False)
    total = models.FloatField(default=0.0, blank=False)
    additional_notes = models.TextField(blank=False)
    due_date = models.DateTimeField(blank=False)
    is_paid = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "invoice"
        verbose_name_plural = "invoices"
        db_table = "Invoices"

    def __str__(self) -> str:
        return f"client: {self.client.client_name} - Due: {self.due_date}"
