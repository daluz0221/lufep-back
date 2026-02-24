
from django.urls import path #type:ignore

from .controllers.home_view import HomeView
from .controllers.admin.home.hero import HomeHeroAdminView, HomeHeroAdminDetailView
from .controllers.admin.home.benefits import HomeBenefitsAdminView, HomeBenefitsAdminDetailView
from .controllers.admin.home.services import HomeServicesAdminView, HomeServicesAdminDetailView
from .controllers.admin.home.how_it_works import HomeHowItWorksAdminView, HomeHowItWorksAdminDetailView
from .controllers.admin.home.about import HomeAboutAdminView, HomeAboutAdminDetailView
from .controllers.admin.home.testimonials import (
    HomeTestimonialsAdminView,
    HomeTestimonialsAdminDetailView,
)


app_name = "cms"

urlpatterns = [
    path('home', HomeView.as_view(), name="home-sctions"),
    path('admin/home/hero', HomeHeroAdminView.as_view(), name="admin-home-hero"),
    path('admin/home/hero/<int:id>', HomeHeroAdminDetailView.as_view(), name="admin-home-hero-detail"),
    
    
    #Benefits home endpoint
    path('admin/home/benefit', HomeBenefitsAdminView.as_view(), name="admin-benefits-section"),
    path('admin/home/benefit/<int:id>', HomeBenefitsAdminDetailView.as_view(), name="admin-benefits-section-detail"),
    
    
    #Service home endpoints
    path('admin/home/services', HomeServicesAdminView.as_view(), name="admin-services-section"),
    path('admin/home/services/<int:id>', HomeServicesAdminDetailView.as_view(), name="admin-services-section-detail"),
    
    
    #How it works home endpoints
    path('admin/home/how-it-works', HomeHowItWorksAdminView.as_view(), name="admin-how-it-works-section"),
    path('admin/home/how-it-works/<int:id>', HomeHowItWorksAdminDetailView.as_view(), name="admin-how-it-works-section-detail"),

    #About home endpoints
    path('admin/home/about', HomeAboutAdminView.as_view(), name="admin-home-about"),
    path('admin/home/about/<int:id>', HomeAboutAdminDetailView.as_view(), name="admin-home-about-detail"),

    #Testimonials home endpoints
    path('admin/home/testimonials', HomeTestimonialsAdminView.as_view(), name="admin-home-testimonials"),
    path('admin/home/testimonials/<int:id>', HomeTestimonialsAdminDetailView.as_view(), name="admin-home-testimonials-detail"),
]