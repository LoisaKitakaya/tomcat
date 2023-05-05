from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, OTPDevice


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("username", "email", "first_name", "last_name", "is_staff")

    search_fields = ("username", "email", "first_name", "last_name")

    list_filter = ("is_staff", "is_superuser", "groups")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdminView(admin.ModelAdmin):
    model = Profile

    list_filter = (
        "created_at",
        "updated_at",
    )


@admin.register(OTPDevice)
class OTPDeviceAdminView(admin.ModelAdmin):
    model = OTPDevice

    list_filter = (
        "created_at",
        "updated_at",
    )
