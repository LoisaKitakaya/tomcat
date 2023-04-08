import pyotp
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Package(models.Model):
    name = models.CharField(max_length=50, blank=False)
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
        verbose_name = "subscriber package"
        verbose_name_plural = "subscriber packages"
        db_table = "SubscriberPackages"

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    workspace_uid = models.CharField(max_length=50, blank=False)
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
