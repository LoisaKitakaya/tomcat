from django.db import models
from users.models import Profile
from teams.models import Workspace

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


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100, blank=False, unique=True)
    category_description = models.TextField(blank=False)

    class Meta:
        verbose_name = "product category"
        verbose_name_plural = "product categories"
        db_table = "ProductCategories"

    def __str__(self) -> str:
        return self.category_name


class ProductSubCategory(models.Model):
    parent = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100, blank=False, unique=True)
    category_description = models.TextField(blank=False)

    class Meta:
        verbose_name = "product sub category"
        verbose_name_plural = "product sub categories"
        db_table = "ProductSubCategories"

    def __str__(self) -> str:
        return self.category_name


class Account(models.Model):
    account_name = models.CharField(max_length=100, blank=False)
    account_type = models.CharField(max_length=50, blank=False)
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


class Budget(models.Model):
    budget_name = models.CharField(max_length=100, blank=False)
    budget_description = models.TextField(blank=False)
    budget_is_active = models.BooleanField(default=True, blank=False)
    budget_amount = models.FloatField(default=0.0, blank=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(TransactionSubCategory, on_delete=models.CASCADE)
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
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(TransactionSubCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "target"
        verbose_name_plural = "targets"
        db_table = "Targets"

    def __str__(self) -> str:
        return self.target_name


class Employee(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    email = models.EmailField(max_length=150, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    ID_number = models.CharField(max_length=100, blank=False)
    employment_status = models.CharField(max_length=20, blank=False)
    job_title = models.CharField(max_length=255, blank=False)
    job_description = models.TextField(blank=False)
    is_manager = models.BooleanField(default=False, blank=False)
    salary = models.FloatField(default=0.0, blank=False)
    department = models.CharField(max_length=255, blank=False)
    employee_id = models.CharField(max_length=50, blank=False)
    emergency_contact_name = models.CharField(max_length=50, blank=False)
    emergency_contact_phone_number = models.CharField(max_length=20, blank=False)
    emergency_contact_email = models.EmailField(max_length=150, blank=True)
    date_of_hire = models.DateField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_of_hire"]
        verbose_name = "employee"
        verbose_name_plural = "employees"
        db_table = "Employees"

    def __str__(self) -> str:
        return self.first_name


class Product(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE)
    buying_price = models.FloatField(default=0.0, blank=False)
    selling_price = models.FloatField(default=0.0, blank=False)
    current_stock_level = models.IntegerField(default=0, blank=False)
    units_sold = models.IntegerField(default=0, blank=False)
    reorder_level = models.IntegerField(default=0, blank=True)
    reorder_quantity = models.IntegerField(default=0, blank=True)
    supplier_name = models.CharField(max_length=255, blank=False)
    supplier_phone_number = models.CharField(max_length=20, blank=False)
    supplier_email = models.CharField(max_length=150, blank=True)
    profit_generated = models.FloatField(default=0.0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "product"
        verbose_name_plural = "products"
        db_table = "Products"

    def __str__(self) -> str:
        return self.name
