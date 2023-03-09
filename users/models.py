from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))


class Profile(models.Model):

    FREE = "free"
    STANDARD = "standard"
    PRO = "pro"

    PROFILE_TIERS = (
        (FREE, "free"),
        (STANDARD, "standard"),
        (PRO, "pro"),
    )

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tier = models.CharField(max_length=20, choices=PROFILE_TIERS, default=FREE)
    account_limit = models.IntegerField(default=2)
    ai_predictions = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"
        db_table = "UserProfiles"

    def __str__(self) -> str:

        return self.user.username
