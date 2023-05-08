from uuid import uuid4
from django.db import models
from accounts.models import Account


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


class CashFlowStatement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    statement_uid = models.CharField(
        max_length=50, blank=False, default=str(uuid4().hex)
    )
    begin_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "cash flow statement"
        verbose_name_plural = "cash flow statements"
        db_table = "CashFlowStatements"

    def __str__(self) -> str:
        return self.statement_uid


class CashFlowItem(models.Model):
    name = models.CharField(max_length=300, blank=False)
    is_income = models.BooleanField(default=False, blank=False)
    activity = models.ForeignKey(BusinessActivity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "cash flow item"
        verbose_name_plural = "cash flow items"
        db_table = "CashFlowItems"

    def __str__(self) -> str:
        return self.name


class CashFlowRecord(models.Model):
    statement_uuid = models.CharField(max_length=50, blank=False)
    amount = models.FloatField(default=0.0, blank=False)
    item = models.ForeignKey(CashFlowItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "cash flow record"
        verbose_name_plural = "cash flow records"
        db_table = "CashFlowRecords"

    def __str__(self) -> str:
        return self.item.name
