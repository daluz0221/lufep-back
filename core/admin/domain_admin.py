from django.contrib import admin
from core.models import Domain


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = (
        "domain",
        "website",
        "tenant",
        "is_primary",
    )

    list_filter = (
        "tenant",
        "website",
        "is_primary",
    )

    search_fields = (
        "domain",
        "website__name",
        "tenant__name",
    )

    ordering = ("tenant", "website", "-is_primary", "domain")

    list_editable = ("is_primary",)

    autocomplete_fields = ("tenant", "website")

    readonly_fields = ()

    fieldsets = (
        (None, {
            "fields": (
                "domain",
                "is_primary",
            )
        }),
        ("Relación", {
            "fields": (
                "tenant",
                "website",
            )
        }),
    )
