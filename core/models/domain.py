from django.db import models



class Domain(models.Model):
    tenant = models.ForeignKey("core.Tenant", on_delete=models.CASCADE)
    website = models.ForeignKey("core.Website", on_delete=models.CASCADE, related_name="domains")
    
    domain = models.CharField(max_length=255, unique=True)
    is_primary = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            Domain.objects.filter(
                website=self.website,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)