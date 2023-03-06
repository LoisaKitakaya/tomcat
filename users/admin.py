from .models import User, Profile, UserLog, WorkSpace
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdminView(admin.ModelAdmin):

    model = Profile

@admin.register(UserLog)
class UserLogAdminView(admin.ModelAdmin):

    model = UserLog

@admin.register(WorkSpace)
class WorkSpaceAdminView(admin.ModelAdmin):

    model = WorkSpace

    list_display = (
        'workspace_name',
        'public_id',
        'workspace_tier',
    )

    list_filter = (
        'workspace_tier',
        'created_at',
        'updated_at',
    )