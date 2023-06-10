from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=50, blank=False)
    accounts = models.BooleanField(default=False, blank=False)
    no_of_accounts = models.IntegerField(default=0, blank=False)
    budgets = models.BooleanField(default=False, blank=False)
    no_of_budgets = models.IntegerField(default=0, blank=False)
    targets = models.BooleanField(default=False, blank=False)
    no_of_targets = models.IntegerField(default=0, blank=False)
    invoices = models.BooleanField(default=False, blank=False)
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
