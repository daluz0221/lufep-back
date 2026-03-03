from typing import Optional, Tuple
from django.http import HttpRequest # type: ignore

from core.models import Domain, Tenant, Website


class TenantResolver:

    @staticmethod
    def from_request(request: HttpRequest) -> Tuple[Optional[Tenant], Optional[Website], bool]:
        host = request.get_host().lower().split(":")[0].rstrip(".")

        is_admin_request = host.startswith("admin.")

        # Admin centralizado: el tenant se resuelve después de autenticar al usuario,
        # no desde la URL. Retornar inmediatamente sin consultar la DB.
        if is_admin_request:
            return None, None, True

        # Peticiones públicas (Astro): resolver tenant/website por dominio.
        search_host = host[4:] if host.startswith("www.") else host

        try:
            domain = Domain.objects.select_related("tenant", "website").get(domain=search_host)
            return domain.tenant, domain.website, False
        except Domain.DoesNotExist:
            return None, None, False
