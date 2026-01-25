from django.contrib import admin
from core.models import Website, HeaderLinks


class HeaderLinksInline(admin.TabularInline):
    model = HeaderLinks
    extra = 1
    ordering = ("order",)


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "type",
        "is_active"
    )
    
    list_filter = ("is_active",)
    search_fields = ("name", "type")
    inlines = [HeaderLinksInline]