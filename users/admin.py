from .models import User, Profile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdminView(admin.ModelAdmin):

    model = Profile

    list_filter = (
        "created_at",
        "updated_at",
    )
