

def tenant_is_active(request):
    return request.tenant and request.tenant.is_active




def user_has_tenant_access(request) -> bool:
    user = getattr(request, "user", None)
    website = getattr(request, "website", None)
    if not user or not user.is_authenticated or not website:
        return False
    if getattr(user, "is_superuser", False):
        return True
    return user.tenant_id == website.tenant_id