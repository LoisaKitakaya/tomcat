import pyotp
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class Package(models.Model):
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    workspace_uid = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=50, blank=True)
    payment_method = models.CharField(max_length=50, blank=False, default="None")
    is_paid_user = models.BooleanField(default=False, blank=False)
    is_employee = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"
        db_table = "UserProfiles"

    def __str__(self) -> str:
        return self.user.email


class OTPDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    key = models.CharField(max_length=100, blank=False, default=pyotp.random_base32())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "user device"
        verbose_name_plural = "user devices"
        db_table = "UserDevices"

    def __str__(self) -> str:
        return self.name
