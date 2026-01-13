from django.contrib import admin
from core.models import Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "type",
        "is_active"
    )
    
    list_filter = ("is_active",)
    search_fields = ("name", "type")