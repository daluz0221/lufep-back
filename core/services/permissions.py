from rest_framework.permissions import BasePermission # type: ignore


class IsAdminOriginPermission(BasePermission):
    """Permite el acceso solo si la petición proviene del subdominio admin."""

    message = "Este endpoint solo es accesible desde el panel de administración."

    def has_permission(self, request, view) -> bool:
        return getattr(request, "is_admin", False)


class TenantAccessPermission(BasePermission):
    """Garantiza que el usuario solo acceda a datos de su propio tenant."""

    message = "No tienes permisos para acceder a este recurso."

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        # El superadmin puede acceder a cualquier tenant.
        if getattr(user, "is_superuser", False):
            return True
        website = request.context.get("website") if hasattr(request, "context") else None
        if not website:
            return False
        return user.tenant_id == website.tenant_id


# Funciones de utilidad conservadas para compatibilidad con código existente.
def tenant_is_active(request) -> bool:
    return bool(request.tenant and request.tenant.is_active)


def user_has_tenant_access(request) -> bool:
    user = getattr(request, "user", None)
    website = getattr(request, "website", None)
    if not user or not user.is_authenticated or not website:
        return False
    if getattr(user, "is_superuser", False):
        return True
    return user.tenant_id == website.tenant_id
