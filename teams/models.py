from uuid import uuid4
from django.db import models
from users.models import User

# Create your models here.
class Workspace(models.Model):

    name = models.CharField(max_length=50, blank=False)
    workspace_uid = models.CharField(
        max_length=50, blank=False, default=str(uuid4().hex)
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "workspace"
        verbose_name_plural = "Workspaces"
        db_table = "Workspaces"

    def __str__(self) -> str:

        return self.name


class TeamLogs(models.Model):

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=150, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]
        verbose_name = "team log"
        verbose_name_plural = "team logs"
        db_table = "TeamLogs"

    def __str__(self) -> str:

        return self.user.email
