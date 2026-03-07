from django.conf import settings as django_settings  # type: ignore
from django.contrib.auth import authenticate  # type: ignore
from django.contrib.auth.password_validation import validate_password  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore

from rest_framework import status  # type: ignore
from rest_framework.permissions import IsAuthenticated, BasePermission  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError  # type: ignore

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


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Establece la cookie HttpOnly con el refresh token en la respuesta."""
    response.set_cookie(
        django_settings.REFRESH_TOKEN_COOKIE_NAME,
        refresh_token,
        max_age=django_settings.REFRESH_TOKEN_COOKIE_MAX_AGE,
        path=django_settings.REFRESH_TOKEN_COOKIE_PATH,
        secure=not django_settings.DEBUG,
        httponly=True,
        samesite="Lax",
    )


class CookieTokenRefreshView(APIView):
    """Devuelve un nuevo access token leyendo el refresh token desde la cookie HttpOnly."""

    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        token = request.COOKIES.get(django_settings.REFRESH_TOKEN_COOKIE_NAME)
        if not token:
            return Response(
                {"detail": "Refresh token no presente en la cookie."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            refresh = RefreshToken(token)
        except TokenError as e:
            raise InvalidToken(str(e)) from e
        return Response(
            {"access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )


class LoginAPIView(APIView):
    """Endpoint de login exclusivo del panel de administración."""

    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        # TODO: desactivar este bloque cuando se tenga las urls de producción.
        # if not getattr(request, "is_admin", False):
        #     return Response(
        #         {"error": "Este endpoint solo es accesible desde el panel de administración."},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

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
        access = str(refresh.access_token)
        refresh_str = str(refresh)

        if user.must_change_password:
            response = Response(
                {
                    "must_change_password": True,
                    "access": access,
                },
                status=status.HTTP_200_OK,
            )
            _set_refresh_cookie(response, refresh_str)
            return response

        websites = list(
            Website.objects
            .filter(tenant=user.tenant, is_active=True)
            .values("id", "name", "type")
        )
        response = Response(
            {
                "must_change_password": False,
                "access": access,
                "websites": websites,
            },
            status=status.HTTP_200_OK,
        )
        _set_refresh_cookie(response, refresh_str)
        return response


def _serialize_user(user: User) -> dict:
    """Serialización mínima del usuario para GET/PATCH me."""
    tenant = user.tenant
    return {
        "id": user.pk,
        "email": user.email,
        "user_type": user.user_type,
        "tenant": (
            {"id": tenant.pk, "name": tenant.name}
            if tenant
            else None
        ),
        "must_change_password": user.must_change_password,
        "date_joined": user.date_joined.isoformat() if user.date_joined else None,
    }


class CurrentUserAPIView(APIView):
    """Devuelve los datos del usuario autenticado. No exige haber cambiado la contraseña."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            _serialize_user(request.user),
            status=status.HTTP_200_OK,
        )


class CurrentUserUpdateAPIView(APIView):
    """Actualiza datos del usuario autenticado. Por ahora el modelo no tiene campos editables."""

    permission_classes = [IsAuthenticated]

    def patch(self, request):
        # Sin campos editables en el modelo User aún; devolver el usuario actual.
        return Response(
            _serialize_user(request.user),
            status=status.HTTP_200_OK,
        )


class ChangePasswordAPIView(APIView):
    """
    Cambio de contraseña para el usuario autenticado.

    Pensada para:
    - Primer acceso: el usuario tiene contraseña temporal (must_change_password=True).
      En ese caso solo se envía new_password.
    - Desde perfil: el usuario ya cambió la contraseña. Debe enviar current_password
      y new_password para validar antes de cambiar.

    Body: new_password (requerido), current_password (opcional; obligatorio si
    must_change_password=False).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get("new_password")
        current_password = request.data.get("current_password")

        if not new_password:
            return Response(
                {"error": "El campo new_password es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        if not user.must_change_password:
            if not current_password:
                return Response(
                    {"error": "El campo current_password es requerido para cambiar la contraseña."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not user.check_password(current_password):
                return Response(
                    {"error": "Contraseña actual incorrecta."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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
