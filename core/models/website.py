from django.db import models
from .base import TenantModel


class Website(TenantModel):
    
    WEBSITE_TYPE_CHOICES = (
        ("info", "Informative"),
        ("portfolio", "Portafolio"),
        ("ecommerce", "Ecommerce")
    )
    
    
    type = models.CharField(max_length=20, choices=WEBSITE_TYPE_CHOICES)
    
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.type})"