
from django.urls import path

from .controllers.home_view import HomeView
from .controllers.admin.home.hero import HomeHeroAdminView, HomeHeroAdminDetailView
from .controllers.admin.home.benefits import HomeBenefitsAdminView, HomeBenefitsAdminDetailView
from .controllers.admin.home.services import HomeServicesAdminView

app_name = "cms"

urlpatterns = [
    path('/home', HomeView.as_view(), name="home-sctions"),
    path('/admin/home/hero', HomeHeroAdminView.as_view(), name="admin-home-hero"),
    path('/admin/home/hero/<int:id>', HomeHeroAdminDetailView.as_view(), name="admin-home-hero-detail"),
    
    
    #Benefits home endpoint
    path('/admin/home/benefit', HomeBenefitsAdminView.as_view(), name="admin-benefits-section"),
    path('/admin/home/benefit/<int:id>', HomeBenefitsAdminDetailView.as_view(), name="admin-benefits-section-detail"),
    
    
    #Service home endpoints
    path('/admin/home/services', HomeServicesAdminView.as_view(), name="admin-services-section"),
]