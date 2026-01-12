

def tenant_is_active(request):
    return request.tenant and request.tenant.is_active