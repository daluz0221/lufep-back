import uuid

from django.db import models
from .base import TimeStampedModel



class Tenant(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    
    


