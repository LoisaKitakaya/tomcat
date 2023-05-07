from django.db import models
from teams.models import Workspace
from accounts.models import Account


class Customer(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    phone = models.CharField(max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "customer"
        verbose_name_plural = "customers"
        db_table = "Customers"

    def __str__(self) -> str:
        return self.name


class Debt(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0, blank=False)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "debt"
        verbose_name_plural = "debts"
        db_table = "Debts"

    def __str__(self) -> str:
        return self.customer.name
