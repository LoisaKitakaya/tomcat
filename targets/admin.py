from django.contrib import admin
from targets.models import Target

# Register your models here.


@admin.register(Target)
class TargetAdminView(admin.ModelAdmin):
    model = Target

    list_display = ("target_name",)

    list_filter = (
        "created_at",
        "updated_at",
    )
