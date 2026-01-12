from django.db import models
from .base import TimeStampedModel



class Plan(models.Model):
    name = models.CharField(max_length=100)
    max_websites = models.PositiveIntegerField()
    has_ecommerce = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    
class Subscription(TimeStampedModel):
    tenant = models.OneToOneField("core.tenant", on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)