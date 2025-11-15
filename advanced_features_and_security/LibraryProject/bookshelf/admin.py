from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields shown in admin list view
    list_display = ("username", "email", "date_of_birth", "is_staff")

    # Fields allowed when editing a user
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields shown when creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "date_of_birth", "profile_photo", "password1", "password2", "is_staff", "is_active"),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
