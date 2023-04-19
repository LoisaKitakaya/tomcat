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
    description = models.TextField(blank=False)  # type: ignore
    transaction_date = models.DateTimeField(blank=False)
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
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
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
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
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


class Employee(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    email = models.EmailField(max_length=150, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    ID_number = models.CharField(max_length=100, blank=False)
    employment_status = models.CharField(max_length=20, blank=False)
    job_title = models.CharField(max_length=255, blank=False)
    is_manager = models.BooleanField(default=False, blank=False)
    salary = models.FloatField(default=0.0, blank=False)
    date_of_hire = models.DateField(blank=False)
    passport = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=255, blank=True)
    job_description = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=50, blank=True)
    emergency_contact_phone_number = models.CharField(max_length=20, blank=True)
    emergency_contact_email = models.EmailField(max_length=150, blank=True)
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
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    sku = models.CharField(max_length=100)
    category = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock_level = models.IntegerField()
    units_sold = models.IntegerField()
    reorder_level = models.IntegerField()
    reorder_quantity = models.IntegerField()
    supplier_name = models.CharField(max_length=255)
    supplier_contact_phone_number = models.CharField(max_length=20)
    supplier_contact_email = models.CharField(max_length=150)
    profit_generated = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "product"
        verbose_name_plural = "products"
        db_table = "Products"

    def __str__(self) -> str:
        return self.name
