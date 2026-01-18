from django.contrib import admin
from apps.showcase.models import (
    HeroSection,
    BenefitsSection,
    Benefit,
    ServiceSection,
    Service,
    HowItWorksSection,
    HowItWorksStep,
    AboutSection, 
    Testimonial,
    TestimonialSection,
    FinalCTASection
)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    
    list_display = (
        "website",
        "headline",
        "subheadline",
        "textCta",
        "imageUrl",
        "is_active"
    )
    
    list_filter = ("is_active", "website")
    search_fields = ("name", "website", "order")
    
class BenefitInline(admin.TabularInline):
    model = Benefit
    extra = 1
    ordering = ("order",)
    

@admin.register(BenefitsSection)
class BenefitSectionAdmin(admin.ModelAdmin):
    list_display = ("website", "title", "is_active", "order")
    list_filter = ("website", "is_active")
    inlines = [BenefitInline]
    
    
class ServiceInline(admin.TabularInline):
    model = Service
    extra = 2
    ordering = ("order",)
    

@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    list_display = ("website", "title", "is_active", "order")
    list_filter = ("website", "is_active")
    inlines = [ServiceInline]
    
    
class HowItWorksStepInline(admin.TabularInline):
    model = HowItWorksStep
    extra = 1
    ordering = ("order",)


@admin.register(HowItWorksSection)
class HowItWorksAdmin(admin.ModelAdmin):
    list_display = ("website", "title", "is_active", "order")
    list_filter = ("website", "is_active")
    inlines = [HowItWorksStepInline]
    
    
@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ("website", "is_active", "order")
    list_filter = ("website", "is_active")
    
    
class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    ordering = ("order",)


@admin.register(TestimonialSection)
class TestimonialSectionAdmin(admin.ModelAdmin):
    list_display = ("website", "title", "is_active", "order")
    list_filter = ("website", "is_active")
    inlines = [TestimonialInline]
    
    
@admin.register(FinalCTASection)
class FinalCTAAdmin(admin.ModelAdmin):
    list_display = ("website", "headline", "is_active", "order")
    list_filter = ("website", "is_active")