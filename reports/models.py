from django.db import models
from accounts.models import Account


class CashFlowRecord(models.Model):
    uid = models.CharField(max_length=50, blank=False)
    category = models.CharField(max_length=100, blank=False)
    item = models.CharField(max_length=100, blank=False)
    activity = models.CharField(max_length=50, blank=False)
    amount = models.FloatField(default=0.0, blank=False)
    is_income = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "cash flow record"
        verbose_name_plural = "cash flow records"
        db_table = "CashFlowRecords"

    def __str__(self) -> str:
        return self.item


class CashFlowStatement(models.Model):
    uid = models.CharField(max_length=50, blank=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    record = models.ForeignKey(CashFlowRecord, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "cash flow statement"
        verbose_name_plural = "cash flow statements"
        db_table = "CashFlowStatements"

    def __str__(self) -> str:
        return self.record.activity


class CashFlowStatementIdentifier(models.Model):
    uid = models.CharField(max_length=50, blank=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    period_start_date = models.DateField(blank=False)
    period_end_date = models.DateField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "cash flow statement identifier"
        verbose_name_plural = "cash flow statements identifiers"
        db_table = "CashFlowStatementsIdentifiers"

    def __str__(self) -> str:
        return (
            f"Cash flow statement - {self.period_start_date} to {self.period_end_date}"
        )


class IncomeStatement(models.Model):
    uid = models.CharField(max_length=50, blank=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    period_start_date = models.DateField(blank=False)
    period_end_date = models.DateField(blank=False)
    revenue = models.FloatField(default=0.0, blank=False)
    gross_profit = models.FloatField(default=0.0, blank=False)
    operating_expenses = models.FloatField(default=0.0, blank=False)
    net_income = models.FloatField(default=0.0, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "income statement"
        verbose_name_plural = "income statements"
        db_table = "IncomeStatements"

    def __str__(self) -> str:
        return (
            f"Cash flow statement - {self.period_start_date} to {self.period_end_date}"
        )


class BalanceSheetStatement(models.Model):
    uid = models.CharField(max_length=50, blank=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    assets = models.FloatField(default=0.0, blank=False)
    liabilities = models.FloatField(default=0.0, blank=False)
    equity = models.FloatField(default=0.0, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "balance sheet statement"
        verbose_name_plural = "balance sheet statements"
        db_table = "BalanceSheetStatements"

    def __str__(self) -> str:
        return f"Cash flow statement of account - {self.account.account_name}"
