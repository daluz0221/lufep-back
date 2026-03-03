from django.contrib.auth import authenticate # type: ignore
from django.contrib.auth.password_validation import validate_password # type: ignore
from django.core.exceptions import ValidationError # type: ignore   

from rest_framework import status # type: ignore
from rest_framework.permissions import IsAuthenticated, BasePermission # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore

from .models.website import Website
from .models.user import User
from .services.throttles import LoginRateThrottle
from .services.permissions import IsAdminOriginPermission, TenantAccessPermission


class PasswordChangedPermission(BasePermission):
    """Bloquea el acceso si el usuario aún debe cambiar su contraseña."""

    message = "Debes cambiar tu contraseña antes de continuar."

    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        user = request.user
        if not user.is_authenticated:
            return False
        return not user.must_change_password


class AdminView(APIView):
    """Clase base para todas las vistas del panel de administración.

    Cadena de permisos:
      1. IsAuthenticated         — requiere JWT válido.
      2. PasswordChangedPermission — bloquea si must_change_password=True.
      3. IsAdminOriginPermission — solo acepta peticiones desde admin.midominio.com.
      4. TenantAccessPermission  — el usuario solo accede a datos de su tenant.
    """

    permission_classes = [
        IsAuthenticated,
        PasswordChangedPermission,
        # IsAdminOriginPermission,
        TenantAccessPermission,
    ]

    def initial(self, request, *args, **kwargs):
        # super().initial() resuelve autenticación y permisos antes de continuar.
        super().initial(request, *args, **kwargs)

        # En este punto request.user ya es el usuario autenticado por JWT.
        # Resolución del website a partir del tenant del usuario.
        website = (
            Website.objects
            .filter(tenant=request.user.tenant, is_active=True)
            .first()
        )
        request.context["website"] = website


class LoginAPIView(APIView):
    """Endpoint de login exclusivo del panel de administración."""

    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        if not getattr(request, "is_admin", False):
            return Response(
                {"error": "Este endpoint solo es accesible desde el panel de administración."},
                status=status.HTTP_403_FORBIDDEN,
            )

        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email y contraseña son requeridos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=email, password=password)

        if not isinstance(user, User):
            return Response(
                {"error": "Credenciales inválidas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)

        if user.must_change_password:
            return Response(
                {
                    "must_change_password": True,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )

        websites = list(
            Website.objects
            .filter(tenant=user.tenant, is_active=True)
            .values("id", "name", "type")
        )

        return Response(
            {
                "must_change_password": False,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "websites": websites,
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordAPIView(APIView):
    """Permite al usuario cambiar su contraseña usando su JWT actual."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get("new_password")

        if not new_password:
            return Response(
                {"error": "El campo new_password es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        try:
            validate_password(new_password, user)
        except ValidationError as exc:
            return Response(
                {"error": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.must_change_password = False
        user.save(update_fields=["password", "must_change_password"])

        return Response(
            {"message": "Contraseña actualizada correctamente."},
            status=status.HTTP_200_OK,
        )
