


class RequestContextMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        request.context = {
            "tenant": getattr(request, "tenant", None),
            "website": getattr(request, "website", None),
            "user": getattr(request, "user", None)
        }
        
        return self.get_response(request)