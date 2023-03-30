from django.db import models
from users.models import Profile
from teams.models import Workspace

# Create your models here.


class Category(models.Model):

    category_name = models.CharField(max_length=100, blank=False, unique=True)
    category_description = models.TextField(blank=False)

    class Meta:

        verbose_name = "category"
        verbose_name_plural = "categories"
        db_table = "Categories"

    def __str__(self) -> str:

        return self.category_name


class Account(models.Model):

    account_name = models.CharField(max_length=100, blank=False)
    account_type = models.CharField(max_length=50, blank=False)
    account_number = models.CharField(max_length=254)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    currency_code = models.CharField(max_length=3, blank=False)
    account_balance = models.FloatField(default=0.0, blank=False)
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

    transaction_type = models.CharField(max_length=50, blank=False)
    transaction_amount = models.FloatField(default=0.0, blank=False)
    currency_code = models.CharField(max_length=3, blank=False)
    description = models.TextField(blank=False)
    transaction_date = models.DateField(blank=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["created_at"]
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
        db_table = "Transactions"

    def __str__(self) -> str:

        return self.transaction_type


class Budget(models.Model):

    budget_name = models.CharField(max_length=100, blank=False)
    budget_description = models.TextField(blank=False)
    budget_is_active = models.BooleanField(default=True, blank=False)
    budget_amount = models.FloatField(default=0.0, blank=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
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


class Target(models.Model):

    target_name = models.CharField(max_length=100, blank=False)
    target_description = models.TextField(blank=False)
    target_is_active = models.BooleanField(default=True, blank=False)
    target_amount = models.FloatField(default=0.0, blank=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "target"
        verbose_name_plural = "targets"
        db_table = "Targets"

    def __str__(self) -> str:

        return self.target_name
