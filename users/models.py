from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.management.utils import get_random_secret_key

# Create your models here.


class User(AbstractUser):

    phone_number = models.CharField(max_length=50)


class Profile(models.Model):

    FREE = "free"
    STANDARD = "standard"
    PRO = "pro"

    PROFILE_TIERS = (
        (FREE, "free"),
        (STANDARD, "standard"),
        (PRO, "pro"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tier = models.CharField(max_length=20, choices=PROFILE_TIERS, default=FREE)
    secret_key = models.CharField(max_length=100, default=str(get_random_secret_key()))
    account_limit = models.IntegerField(default=1)
    budget_limit = models.IntegerField(default=4)
    pdf_gen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"
        db_table = "UserProfiles"

    def __str__(self) -> str:

        return self.user.username
