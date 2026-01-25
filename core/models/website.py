from typing import TYPE_CHECKING

from django.db import models
from .base import TenantModel

if TYPE_CHECKING:
    from core.models.domain import Domain

class Website(TenantModel):
    
    WEBSITE_TYPE_CHOICES = (
        ("info", "Informative"),
        ("portfolio", "Portafolio"),
        ("ecommerce", "Ecommerce")
    )
    
    
    type = models.CharField(max_length=20, choices=WEBSITE_TYPE_CHOICES)
    
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    
    domains: "models.Manager[Domain]"
    def __str__(self):
        return f"{self.name} ({self.type})"
    
    
    
class HeaderLinks(models.Model):
    HEADER_LINKS_CHOICES = (
        ("Productos", "Productos"),
        ("Contacto", "Contacto"),
        ("Nosotros", "Nosotros"),
        ("Servicios", "Servicios"),
    )
    
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="header_links")
    type = models.CharField(max_length=25, choices=HEADER_LINKS_CHOICES)
    is_Active = models.BooleanField(default=True)
    
    order = models.PositiveIntegerField(default=0)
    
    
    def to_dict(self):
        return {
            "link": self.type,
            "is_active": self.is_Active
        }