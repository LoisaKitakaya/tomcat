from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    
class Profile(models.Model):

    public_id = models.CharField(max_length=40, default=str(uuid4().hex))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ['-created_at']
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'
        db_table = 'UserProfiles'

    def __str__(self) -> str:
        
        return self.user.username
