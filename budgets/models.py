from django.db import models
from users.models import Profile
from teams.models import Workspace
from accounts.models import Account
from transactions.models import TransactionCategory, TransactionSubCategory


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
