from django.db import models
from accounts.models import Account


class TransactionType(models.Model):
    RECEIVABLE = "receivable"
    PAYABLE = "payable"

    TYPE_CHOICES = (
        (RECEIVABLE, "Receivable"),
        (PAYABLE, "Payable"),
    )

    type_name = models.CharField(max_length=100, blank=False, choices=TYPE_CHOICES)
    type_description = models.TextField(blank=False)

    class Meta:
        verbose_name = "transaction type"
        verbose_name_plural = "transaction types"
        db_table = "TransactionTypes"

    def __str__(self) -> str:
        return self.type_name


class BusinessActivity(models.Model):
    OPERATING_ACTIVITY = "Operating Activity"
    INVESTING_ACTIVITY = "Investing Activity"
    FINANCING_ACTIVITY = "Financing Activity"

    ACTIVITY_CHOICES = (
        (OPERATING_ACTIVITY, "Operating"),
        (INVESTING_ACTIVITY, "Investing"),
        (FINANCING_ACTIVITY, "Financing"),
    )

    name = models.CharField(max_length=50, blank=False, choices=ACTIVITY_CHOICES)

    class Meta:
        verbose_name = "business activity"
        verbose_name_plural = "Business activities"
        db_table = "BusinessActivities"

    def __str__(self) -> str:
        return self.name


class TransactionGroup(models.Model):
    activity = models.ForeignKey(BusinessActivity, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100, blank=False, unique=True)

    class Meta:
        verbose_name = "transaction group"
        verbose_name_plural = "transaction groups"
        db_table = "TransactionGroups"

    def __str__(self) -> str:
        return self.group_name


class TransactionCategory(models.Model):
    parent = models.ForeignKey(TransactionGroup, on_delete=models.CASCADE)
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
    description = models.TextField(blank=False)
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
