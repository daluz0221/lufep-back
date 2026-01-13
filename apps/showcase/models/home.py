from django.db import models
from core.models import TimeStampedModel, Website


class HeroSection(TimeStampedModel):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    
    headline = models.CharField(max_length=250, blank=True, null=True)
    subheadline = models.CharField(max_length=450, blank=True, null=True)
    
    imageUrl = models.CharField()
    textCta = models.CharField(max_length=200)
    
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"Hero Section content for {self.website} with domain {self.website.domains.get(is_primary=True)}"