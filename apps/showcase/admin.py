from django.contrib import admin #type: ignore
from apps.showcase.models import (
    HeroSection,
    BenefitsSection,
    Benefit,
    ProductSection,
    Product,
    HowItWorksSection,
    HowItWorksStep,
    AboutSection,
    AboutMetric,
    Testimonial,
    TestimonialSection,
    FinalCTASection,
    AboutIntroSection,
    AboutHistorySection,
    AboutVisionSection,
    AboutDifferentiatorsSection,
    AboutDifferentiator,
    AboutTeamSection,
    AboutVisionItem,
    AboutTeamMember,
)


# Home

# Hero
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "website",
        "headline",
        "subheadline",
        "textCta",
        "imageUrl",
        "is_active",
        "is_deleted",
    )
    list_editable = ("is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted", "website")
    search_fields = ("name", "website", "order")
    
# Benefits
class BenefitInline(admin.TabularInline):
    model = Benefit
    extra = 1
    ordering = ("order",)
    

@admin.register(BenefitsSection)
class BenefitSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")
    inlines = [BenefitInline]
    
    
# Products
class ProductInline(admin.TabularInline):
    model = Product
    extra = 2
    ordering = ("order",)


@admin.register(ProductSection)
class ProductSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")
    inlines = [ProductInline]
    
    
# How it works
class HowItWorksStepInline(admin.TabularInline):
    model = HowItWorksStep
    extra = 1
    ordering = ("order",)


@admin.register(HowItWorksSection)
class HowItWorksAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")
    inlines = [HowItWorksStepInline]
    
    
# About
class AboutMetricInline(admin.TabularInline):
    model = AboutMetric
    extra = 1
    ordering = ("order",)


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")
    inlines = [AboutMetricInline]
    
    
# Testimonials
class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    ordering = ("order",)


@admin.register(TestimonialSection)
class TestimonialSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")
    inlines = [TestimonialInline]
    
    
# CTA
@admin.register(FinalCTASection)
class FinalCTAAdmin(admin.ModelAdmin):
    
    list_display = ("id", "website", "headline", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")

# AboutPage

    
# Intro
@admin.register(AboutIntroSection)
class AboutIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")

# History
@admin.register(AboutHistorySection)
class AboutHistorySectionAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")

# Vision
class AboutVisionItemInline(admin.TabularInline):
    model = AboutVisionItem
    extra = 1
    ordering = ("order",)
    
@admin.register(AboutVisionSection)
class AboutVisionSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")
    inlines = [AboutVisionItemInline]

# Differentiators
class AboutDifferentiatorInline(admin.TabularInline):
    model = AboutDifferentiator
    extra = 1
    ordering = ("order",)
    
@admin.register(AboutDifferentiatorsSection)
class AboutDifferentiatorsSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")
    inlines = [AboutDifferentiatorInline]

# Team
class AboutTeamMemberInline(admin.TabularInline):
    model = AboutTeamMember
    extra = 1
    ordering = ("order",)
    
@admin.register(AboutTeamSection)
class AboutTeamSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "title", "is_active", "is_deleted", "order")
    list_editable = ("is_active", "is_deleted")
    list_filter = ("website", "is_active", "is_deleted")
    inlines = [AboutTeamMemberInline]