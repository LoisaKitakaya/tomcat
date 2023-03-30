from django.contrib import admin
from teams.models import Workspace, TeamLogs

# Register your models here.
@admin.register(Workspace)
class WorkspaceAdminView(admin.ModelAdmin):

    model = Workspace

    list_display = ("name",)

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(TeamLogs)
class TeamLogsAdminView(admin.ModelAdmin):

    model = TeamLogs

    list_filter = (
        "workspace",
        "created_at",
        "updated_at",
    )
