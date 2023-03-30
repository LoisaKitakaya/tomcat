from django.db import models
from users.models import User

# Create your models here.


class CardPaymentMethod(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=255, blank=False)
    card_number = models.CharField(max_length=16, blank=False)
    expiration_month = models.PositiveSmallIntegerField(blank=False)
    expiration_year = models.PositiveSmallIntegerField(blank=False)
    cvc = models.CharField(max_length=4, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "card user"
        verbose_name_plural = "card users"
        db_table = "CardUsers"

    def __str__(self) -> str:

        return self.cardholder_name


class MpesaPaymentMethod(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_owner = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "mpesa user"
        verbose_name_plural = "mpesa users"
        db_table = "MpesaUsers"

    def __str__(self) -> str:

        return self.phone_owner


class CardBilling(models.Model):

    customer = models.ForeignKey(CardPaymentMethod, on_delete=models.CASCADE)
    transaction_uid = models.CharField(max_length=200, blank=False)
    amount = models.FloatField(default=0.0, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "card payment"
        verbose_name_plural = "card payments"
        db_table = "CardPayments"

    def __str__(self) -> str:

        return self.customer.cardholder_name


class MpesaBilling(models.Model):

    customer = models.ForeignKey(MpesaPaymentMethod, on_delete=models.CASCADE)
    transaction_uid = models.CharField(max_length=200, blank=False)
    amount = models.FloatField(default=0.0, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "mpesa payment"
        verbose_name_plural = "mpesa payments"
        db_table = "MpesaPayments"

    def __str__(self) -> str:

        return self.customer.phone_owner
