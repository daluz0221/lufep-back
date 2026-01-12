from typing import Optional, Tuple
from django.http import HttpRequest

from core.models import Domain, Tenant, Website

class TenantResolver:
    
    
    @staticmethod
    def from_request(request:HttpRequest) -> Tuple[Optional[Tenant], Optional[Website]]:
        host = request.get_host().split(":")[0]
        
        try:
            domain = Domain.objects.select_related(
                "tenant", "website"
            ).get(domain=host)
            
            return domain.tenant, domain.website
        except Domain.DoesNotExist:
            return None, None