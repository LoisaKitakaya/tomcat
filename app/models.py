from django.db import models
from users.models import Profile

# Create your models here.


class Category(models.Model):

    category_name = models.CharField(max_length=100)
    category_description = models.CharField(max_length=255)

    class Meta:

        verbose_name = "category"
        verbose_name_plural = "categories"
        db_table = "Categories"

    def __str__(self) -> str:

        return self.category_name


class Account(models.Model):

    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50)
    account_number = models.CharField(max_length=254)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    currency_code = models.CharField(max_length=3)
    account_balance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "account"
        verbose_name_plural = "accounts"
        db_table = "Accounts"

    def __str__(self) -> str:

        return self.account_name


class Transaction(models.Model):

    transaction_type = models.CharField(max_length=50)
    transaction_amount = models.FloatField()
    currency_code = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    transaction_date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
        db_table = "Transactions"

    def __str__(self) -> str:

        return self.transaction_type


class Budget(models.Model):

    budget_name = models.CharField(max_length=100)
    budget_description = models.CharField(max_length=255)
    budget_is_active = models.BooleanField(default=True)
    budget_amount = models.DecimalField(max_digits=15, decimal_places=2)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "budget"
        verbose_name_plural = "budgets"
        db_table = "Budgets"

    def __str__(self) -> str:

        return self.budget_name
