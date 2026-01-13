from django.contrib import admin
from apps.showcase.models import (
    HeroSection
)


@admin.register(HeroSection)
class WebsiteAdmin(admin.ModelAdmin):
    
    list_display = (
        "website",
        "headline",
        "subheadline",
        "textCta",
        "imageUrl",
        "is_active"
    )
    
    list_filter = ("is_active", "website")
    search_fields = ("name", "website")