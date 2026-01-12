from core.services import TenantResolver


class TenantMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        tenant, website = TenantResolver.from_request(request)
        
        request.tenant = tenant
        request.website = website
        
        
        return self.get_response(request)
    
    