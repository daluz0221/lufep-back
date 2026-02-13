
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginAPIView


app_name = "core"

urlpatterns = [
    path('/login', LoginAPIView.as_view(), name="Login"),
    path('/token/refresh', TokenRefreshView.as_view(), name="token_refresh")   
]


