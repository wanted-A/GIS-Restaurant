from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "username",
                    "email",
                    # "user_lat", #위도
                    # "user_lon", #경도
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )
    
    readonly_fields = ("last_login", "date_joined")

    list_display = (
        "id",
        "username",
        "email",
        # "user_lat", #위도
        # "user_lon", #경도
        "is_active",
        "is_admin",
    )
    list_display_links = (
        "id",
        "username",
        "email",
        # "user_lat", #위도
        # "user_lon", #경도
    )
    list_filter = (
        "is_active",
        "is_admin",
        # "user_lat", #위도
        # "user_lon", #경도
    )
