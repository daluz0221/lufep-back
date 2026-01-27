from typing import TYPE_CHECKING
from django.db import models
from core.models import Website

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager
class BaseSection(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)


    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True



class HeroSection(BaseSection):
    headline = models.CharField(max_length=250, blank=True, null=True)
    highlight_word = models.CharField(max_length=150, blank=True, null=True)
    subheadline = models.CharField(max_length=450, blank=True, null=True)
    
    imageUrl = models.CharField()
    imageAlt = models.CharField(default="")
    textCta = models.CharField(max_length=200)
    urlCta = models.CharField(max_length=250)
    
    
    def __str__(self):
        return f"Hero Section content for {self.website}"
    
    def to_dict(self):
        return {
            "id": self.pk,
            "headline": self.headline,
            "highlightWord": self.highlight_word,
            "subheadline": self.subheadline,
            "imageUrl": self.imageUrl,
            "imageAlt": self.imageAlt,
            "textCta": self.textCta,
            "urlCta": self.urlCta
        }
        
    
    class Meta(BaseSection.Meta):
        verbose_name = "Home - Hero Section"
        verbose_name_plural = "Home - Hero Section"
    
class BenefitsSection(BaseSection):

    title = models.CharField(max_length=200, default="¿Por qué elegirnos?")
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    
    benefits: "RelatedManager[Benefit]"
    
    
    def __str__(self):
        return f"Benefits home section | {self.website.name}"
    
    def to_dict(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "items": [
                benefit.to_dict()
                for benefit in self.benefits.all().order_by("order")
            ]
        }
    
    class Meta(BaseSection.Meta):
        verbose_name = "Home - Benefits Section"
        verbose_name_plural = "Home - Benefits Section"
    

class Benefit(models.Model):
    section = models.ForeignKey(BenefitsSection, on_delete=models.CASCADE, related_name="benefits")
    
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, blank=True, null=True)
    
    order = models.PositiveIntegerField(default=0)
    
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "icon": self.icon
        }
    
    
class ServiceSection(BaseSection):
    
    title = models.CharField(max_length=200, default="Servicios")
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    url = models.CharField(default="")
    
    servicios: "RelatedManager[Service]"
    
    
    def __str__(self):
        return f"Servicios home | {self.website.name}"
    
    def to_dict(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "url": self.url,
            "items": [
                service.to_dict()
                for service in self.servicios.all().order_by("order")
            ]
        }
    
    class Meta(BaseSection.Meta):
        verbose_name = "Home - Services Section"
        verbose_name_plural = "Home - Services Section"

class Service(models.Model):
    
    section = models.ForeignKey(ServiceSection, on_delete=models.CASCADE, related_name="servicios")
    
    name = models.CharField(max_length=150)
    short_description = models.CharField(max_length=250)
    description = models.TextField()
    image = models.CharField(blank=True, null=True)
    url_text = models.CharField(max_length=150,blank=True, null=True)
    ur = models.CharField(max_length=255)
    
    order = models.PositiveIntegerField(default=0)
    
    def to_dict(self):
        return {
            "name": self.name,
            "shortDescription": self.short_description,
            "description": self.description,
            "image": self.image,
            "urlText": self.url_text,
            "url": self.ur
        }
    
    

class HowItWorksSection(BaseSection):
    title = models.CharField(max_length=200, default="Cómo funciona")
    steps: "RelatedManager[HowItWorksStep]"
    
    def to_dict(self):
        return {
            "title": self.title,
            "items": [
                step.to_dict()
                for step in self.steps.all().order_by("order")
            ]
        }
    
    class Meta(BaseSection.Meta):
        verbose_name = "Home - How it works Section"
        verbose_name_plural = "Home - How it works Section"
    
    
class HowItWorksStep(models.Model):
    
    section = models.ForeignKey(HowItWorksSection, on_delete=models.CASCADE, related_name="steps")
    
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description
        }
    
    
class AboutSection(BaseSection):
    
    title = models.CharField(default="")
    text = models.TextField(max_length=500)
    cta_text = models.CharField(max_length=100)
    cta_url = models.CharField(max_length=255)
    
    metrics: "RelatedManager[AboutMetric]"

    def __str__(self):
        return f"About Teaser | {self.website.name}"
    
    def to_dict(self):
        return {
            "title": self.title,
            "text": self.text,
            "ctaText": self.cta_text,
            "ctaUrl": self.cta_url,
            "items": [
                metric.to_dict()
                for metric in self.metrics.all().order_by("order")
            ]
        }
    
    class Meta(BaseSection.Meta):
        verbose_name = "Home - about Section"
        verbose_name_plural = "Home - about Section"
    

class AboutMetric(models.Model):
    
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name="metrics")
    
    metric = models.CharField(max_length=150, default="")
    text = models.CharField(max_length=250, default="")
    
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.metric}"
    
    def to_dict(self):
        return {
            "metrica": self.metric,
            "text": self.text
        }


class TestimonialSection(BaseSection):
    title = models.CharField(
        max_length=200,
        default="Confían en nosotros"
    )
    
    testimonials: "RelatedManager[Testimonial]"
    metrics: "RelatedManager[TertimonialMetric]"
    def to_dict(self):
        return {
            "title": self.title,
            "testimonios": [
                testimonial.to_dict()
                for testimonial in self.testimonials.all().order_by("order")
            ],
            "metricas": [
                metric.to_dict()
                for metric in self.metrics.all().order_by("order")
            ]
        }
    
    class Meta(BaseSection.Meta):
        verbose_name = "Home - Testimonial Section"
        verbose_name_plural = "Home - Testimonial Section"
    
    
class Testimonial(models.Model):
    section = models.ForeignKey(
        TestimonialSection,
        on_delete=models.CASCADE,
        related_name="testimonials"
    )

    author = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True)
    content = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(default=3)

    order = models.PositiveIntegerField(default=0)
    
    def to_dict(self):
        return {
            "author": self.author,
            "role": self.role,
            "content": self.content
        }
    

class TertimonialMetric(models.Model):
    section = models.ForeignKey(
        TestimonialSection,
        on_delete=models.CASCADE,
        related_name="metrics"
    )    
    
    metric = models.CharField(default="", max_length=150)
    text = models.CharField(default="", max_length=150)
    
    order = models.PositiveIntegerField(default=0)
    
    def to_dict(self):
        return {
            "metrica": self.metric,
            "text": self.text
        }
    
class FinalCTASection(BaseSection):
    headline = models.CharField(max_length=200)
    subheadline = models.CharField(max_length=250)
    button_text = models.CharField(max_length=100)
    button_url = models.CharField(max_length=255)

    def __str__(self):
        return f"Final CTA | {self.website.name}"
    
    def to_dict(self):
        return {
            "headline": self.headline,
            "subheadline": self.subheadline,
            "buttonText": self.button_text,
            "buttonUrl": self.button_url
        }
    
    class Meta(BaseSection.Meta):
        verbose_name = "Home - CTA Section"
        verbose_name_plural = "Home - CTA Section"