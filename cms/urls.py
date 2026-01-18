
from django.urls import path

from .controllers.home_view import HomeView

app_name = "cms"

urlpatterns = [
    path('/home', HomeView.as_view(), name="home-sctions"),
    
]