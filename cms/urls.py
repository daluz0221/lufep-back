
from django.urls import path

from .controllers.home_view import HomeView
from .controllers.admin.home.hero import HomeHeroAdminView, HomeHeroAdminDetailView
from .controllers.admin.home.benefits import HomeBenefitsAdminView, HomeBenefitsAdminDetailView

app_name = "cms"

urlpatterns = [
    path('/home', HomeView.as_view(), name="home-sctions"),
    path('/admin/home/hero', HomeHeroAdminView.as_view(), name="admin-home-hero"),
    path('/admin/home/hero/<int:id>', HomeHeroAdminDetailView.as_view(), name="admin-home-hero-detail"),
    
    
    #Benefits endpoint
    path('/admin/home/benefit', HomeBenefitsAdminView.as_view(), name="admin-benefits-section"),
    path('/admin/home/benefit/<int:id>', HomeBenefitsAdminDetailView.as_view(), name="admin-benefits-section-detail"),
]