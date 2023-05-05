from django.db import models
from accounts.models import Account

# Create your models here.


class TransactionType(models.Model):
    type_name = models.CharField(max_length=100, blank=False, unique=True)
    type_description = models.TextField(blank=False)

    class Meta:
        verbose_name = "transaction type"
        verbose_name_plural = "transaction types"
        db_table = "TransactionTypes"

    def __str__(self) -> str:
        return self.type_name


class TransactionCategory(models.Model):
    category_name = models.CharField(max_length=100, blank=False, unique=True)
    category_description = models.TextField(blank=False)

    class Meta:
        verbose_name = "transaction category"
        verbose_name_plural = "transaction categories"
        db_table = "TransactionCategories"

    def __str__(self) -> str:
        return self.category_name


class TransactionSubCategory(models.Model):
    parent = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100, blank=False, unique=True)
    category_description = models.TextField(blank=False)

    class Meta:
        verbose_name = "transaction sub category"
        verbose_name_plural = "transaction sub categories"
        db_table = "TransactionSubCategories"

    def __str__(self) -> str:
        return self.category_name


class Transaction(models.Model):
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    transaction_amount = models.FloatField(default=0.0, blank=False)
    currency_code = models.CharField(max_length=3, blank=False)
    description = models.TextField(blank=False)  # type: ignore
    transaction_date = models.DateTimeField(blank=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(TransactionSubCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
        db_table = "Transactions"

    def __str__(self) -> str:
        return self.transaction_type.type_name
