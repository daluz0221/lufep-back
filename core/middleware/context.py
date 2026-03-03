class RequestContextMiddleware:
    """Propaga los datos resueltos por TenantMiddleware a request.context.

    Nota: 'user' no se incluye aquí porque en este punto del stack solo está
    disponible el usuario de sesión Django, nunca el usuario autenticado por JWT.
    El website para peticiones admin se completa posteriormente en AdminView.initial().
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.context = {
            "tenant": getattr(request, "tenant", None),
            "website": getattr(request, "website", None),
            "is_admin": getattr(request, "is_admin", False),
        }

        return self.get_response(request)
