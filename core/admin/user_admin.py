from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    ordering = ("email",)
    list_display = (
        "email",
        "user_type",
        "tenant",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "user_type",
        "tenant",
        "is_active",
    )

    search_fields = ("email",)

    fieldsets = (
        ("Credenciales", {
            "fields": ("email", "password")
        }),
        ("Información", {
            "fields": ("user_type", "tenant")
        }),
        ("Permisos", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Fechas", {
            "fields": ("last_login",)
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "user_type",
                "tenant",
                "is_active",
                "is_staff",
            ),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")
