import pyotp
from django.db import models
from billing.models import Plan
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
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
