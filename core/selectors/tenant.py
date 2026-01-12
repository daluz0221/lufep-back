from core.models import Tenant


def get_active_tenant(slug: str) -> Tenant:
    return Tenant.objects.get(slug=slug, is_active=True)