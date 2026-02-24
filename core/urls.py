
from django.urls import path #type: ignore

from rest_framework_simplejwt.views import TokenRefreshView # type: ignore

from .views import LoginAPIView, ChangePasswordAPIView


app_name = "core"

urlpatterns = [
    path('login', LoginAPIView.as_view(), name="Login"),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('reset-password', ChangePasswordAPIView.as_view(), name="change-password")
]


