from django.urls import path  # type: ignore

from .views import (
    LoginAPIView,
    CookieTokenRefreshView,
    CurrentUserAPIView,
    CurrentUserUpdateAPIView,
    ChangePasswordAPIView,
)

app_name = "core"

urlpatterns = [
    path("login", LoginAPIView.as_view(), name="login"),
    path("token/refresh", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("me", CurrentUserAPIView.as_view(), name="me"),
    path("me/change-password", ChangePasswordAPIView.as_view(), name="me-change-password"),
    path("reset-password", ChangePasswordAPIView.as_view(), name="change-password"),
]


