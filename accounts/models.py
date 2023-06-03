from django.db import models
from users.models import Profile


class Account(models.Model):
    account_name = models.CharField(max_length=100, blank=False)
    account_type = models.CharField(max_length=50, blank=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)  # type: ignore
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
