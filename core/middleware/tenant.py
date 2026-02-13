from core.services import TenantResolver


class TenantMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        tenant, website, is_admin = TenantResolver.from_request(request)
        
        request.tenant = tenant
        request.website = website
        request.is_admin = is_admin
        
        return self.get_response(request)
    
    