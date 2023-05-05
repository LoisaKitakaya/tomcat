from django.db import models
from users.models import User

# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length=50, blank=False)
    inventory = models.BooleanField(default=False, blank=False)
    accounts = models.BooleanField(default=False, blank=False)
    no_of_accounts = models.IntegerField(default=0, blank=False)
    budgets = models.BooleanField(default=False, blank=False)
    no_of_budgets = models.IntegerField(default=0, blank=False)
    targets = models.BooleanField(default=False, blank=False)
    no_of_targets = models.IntegerField(default=0, blank=False)
    teams = models.BooleanField(default=False, blank=False)
    no_of_teams = models.IntegerField(default=0, blank=False)
    pdf_reports = models.BooleanField(default=False, blank=False)
    ai_assistant = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "subscriber plan"
        verbose_name_plural = "subscriber plans"
        db_table = "SubscriberPlans"

    def __str__(self) -> str:
        return self.name


class PlanBilling(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_tracking_id = models.CharField(max_length=200, blank=False)
    merchant_ref = models.CharField(max_length=50, blank=False)
    account_ref = models.CharField(max_length=50, blank=True)
    redirect_url = models.URLField(blank=False)
    plan = models.CharField(max_length=10, blank=False)
    currency = models.CharField(max_length=5, blank=False)
    amount = models.FloatField(default=0.0, blank=False)
    payment_confirmed = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "subscription payment"
        verbose_name_plural = "subscription payments"
        db_table = "SubscriptionPayments"

    def __str__(self) -> str:
        return self.customer.username
