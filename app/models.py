from uuid import uuid4
from django.db import models
from users.models import WorkSpace

# Create your models here.

class Account(models.Model):

    CHECKING = 'checking'
    SAVING = 'saving'
    CREDIT = 'credit'
    INVESTMENT = 'investment'
    RETIREMENT = 'retirement'
    LOAN = 'loan'
    INSURANCE = 'insurance'
    MORTGAGE = 'mortgage'

    ACCOUNT_TYPES = (
        (CHECKING, 'Checking'),
        (SAVING, 'Saving'),
        (CREDIT, 'Credit'),
        (INVESTMENT, 'Investment'),
        (RETIREMENT, 'Retirement'),
        (LOAN, 'Loan'),
        (INSURANCE, 'Insurance'),
        (MORTGAGE, 'Mortgage'),
    )

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES, default=CHECKING)
    currency_code = models.CharField(max_length=3)
    account_balance = models.DecimalField(max_digits=15, decimal_places=2)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ['-created_at']
        verbose_name = 'account'
        verbose_name_plural = 'accounts'
        db_table = 'Accounts'

    def __str__(self) -> str:
        
        return self.account_name

class Transaction(models.Model):

    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'
    PAYMENT = 'payment'

    TRANSACTION_TYPES = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer'),
        (PAYMENT, 'Payment')
    )

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    transaction_amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency_code = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    transaction_date = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ['-created_at']
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
        db_table = 'Transactions'

    def __str__(self) -> str:
        
        return self.transaction_type

class Category(models.Model):

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    category_name = models.CharField(max_length=100)
    category_description = models.CharField(max_length=255)

    class Meta:

        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'Categories'

    def __str__(self) -> str:
        
        return self.category_name

class Budget(models.Model):

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    budget_name = models.CharField(max_length=100)
    budget_description = models.CharField(max_length=255)
    budget_start_date = models.DateTimeField()
    budget_end_date = models.DateTimeField()
    budget_amount = models.DecimalField(max_digits=15, decimal_places=2)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ['-created_at']
        verbose_name = 'budget'
        verbose_name_plural = 'budgets'
        db_table = 'Budgets'

    def __str__(self) -> str:
        
        return self.budget_name

class BudgetCategory(models.Model):

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'budget category'
        verbose_name_plural = 'budget categories'
        db_table = 'BudgetCategories'

    def __str__(self) -> str:
        
        return self.budget.budget_name

class TransactionCategory(models.Model):

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'transaction category'
        verbose_name_plural = 'transaction categories'
        db_table = 'TransactionCategories'

    def __str__(self) -> str:
        
        return self.transaction.transaction_type

class Report(models.Model):

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    report_name = models.CharField(max_length=100)
    report_description = models.CharField(max_length=255)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE)
    transactions = models.ManyToManyField(Transaction)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ['-created_at']
        verbose_name = 'report'
        verbose_name_plural = 'reports'
        db_table = 'Reports'

    def __str__(self) -> str:
        
        return self.report_name

class ReportCategory(models.Model):

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'report category'
        verbose_name_plural = 'report categories'
        db_table = 'ReportCategories'

    def __str__(self) -> str:
        
        return self.report.report_name
