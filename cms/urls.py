
from django.urls import path

from .controllers.home_view import HomeView
from .controllers.admin.home.hero import HomeHeroAdminView, HomeHeroDetailView

app_name = "cms"

urlpatterns = [
    path('/home', HomeView.as_view(), name="home-sctions"),
    path('/admin/home/hero', HomeHeroAdminView.as_view(), name="admin-home-hero"),
    path('/admin/home/hero/<int:id>', HomeHeroDetailView.as_view(), name="admin-home-hero-detail"),
    
]