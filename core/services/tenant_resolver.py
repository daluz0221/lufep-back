from typing import Optional, Tuple
from django.http import HttpRequest

from core.models import Domain, Tenant, Website

class TenantResolver:
    
    
    @staticmethod
    def from_request(request:HttpRequest) -> Tuple[Optional[Tenant], Optional[Website], Optional[bool]]:
        host = request.get_host()
        host = host.lower().split(":")[0].rstrip(".")
        
        
        is_admin_request = host.startswith("admin.")
        
        search_host = host[6:] if is_admin_request else host

        if search_host.startswith("www."):
            search_host = search_host[4:]
      
        try:
            domain = Domain.objects.select_related(
                "tenant", "website"
            ).get(domain=search_host)
            return domain.tenant, domain.website, is_admin_request
        except Domain.DoesNotExist:
            return None, None, is_admin_request