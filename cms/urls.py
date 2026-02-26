
from django.urls import path #type:ignore

from .controllers.home_view import HomeView
from .controllers.admin.home.hero import HomeHeroAdminView, HomeHeroAdminDetailView
from .controllers.admin.home.benefits import HomeBenefitsAdminView, HomeBenefitsAdminDetailView
from .controllers.admin.home.products import HomeProductsAdminView, HomeProductsAdminDetailView
from .controllers.admin.home.how_it_works import HomeHowItWorksAdminView, HomeHowItWorksAdminDetailView
from .controllers.admin.home.about import HomeAboutAdminView, HomeAboutAdminDetailView
from .controllers.admin.home.testimonials import (
    HomeTestimonialsAdminView,
    HomeTestimonialsAdminDetailView,
)
from .controllers.admin.home.cta import HomeCTAAdminView, HomeCTAAdminDetailView
from .controllers.about_view import AboutView
from .controllers.admin.about.intro import AboutIntroAdminView, AboutIntroAdminDetailView
from .controllers.admin.about.history import AboutHistoryAdminView, AboutHistoryAdminDetailView
app_name = "cms"

urlpatterns = [
    path('home', HomeView.as_view(), name="home-sctions"),
    
    
    
    #Hero home endpoints
    path('admin/home/hero', HomeHeroAdminView.as_view(), name="admin-home-hero"),
    path('admin/home/hero/<int:id>', HomeHeroAdminDetailView.as_view(), name="admin-home-hero-detail"),
    
    
    #Benefits home endpoint
    path('admin/home/benefit', HomeBenefitsAdminView.as_view(), name="admin-benefits-section"),
    path('admin/home/benefit/<int:id>', HomeBenefitsAdminDetailView.as_view(), name="admin-benefits-section-detail"),
    
    
    #Products home endpoints
    path('admin/home/products', HomeProductsAdminView.as_view(), name="admin-products-section"),
    path('admin/home/products/<int:id>', HomeProductsAdminDetailView.as_view(), name="admin-products-section-detail"),
    
    
    #How it works home endpoints
    path('admin/home/how-it-works', HomeHowItWorksAdminView.as_view(), name="admin-how-it-works-section"),
    path('admin/home/how-it-works/<int:id>', HomeHowItWorksAdminDetailView.as_view(), name="admin-how-it-works-section-detail"),

    #About home endpoints
    path('admin/home/about', HomeAboutAdminView.as_view(), name="admin-home-about"),
    path('admin/home/about/<int:id>', HomeAboutAdminDetailView.as_view(), name="admin-home-about-detail"),

    #Testimonials home endpoints
    path('admin/home/testimonials', HomeTestimonialsAdminView.as_view(), name="admin-home-testimonials"),
    path('admin/home/testimonials/<int:id>', HomeTestimonialsAdminDetailView.as_view(), name="admin-home-testimonials-detail"),
    
    #CTA home endpoints
    path('admin/home/cta', HomeCTAAdminView.as_view(), name="admin-home-cta"),
    path('admin/home/cta/<int:id>', HomeCTAAdminDetailView.as_view(), name="admin-home-cta-detail"),
    
    # Público
    path('about', AboutView.as_view(), name="about-page"),

    # # Admin - Intro
    path('admin/about/intro', AboutIntroAdminView.as_view(), name="admin-about-intro"),
    path('admin/about/intro/<int:id>', AboutIntroAdminDetailView.as_view(), name="admin-about-intro-detail"),

    # Admin - History
    path('admin/about/history', AboutHistoryAdminView.as_view(), name="admin-about-history"),
    path('admin/about/history/<int:id>', AboutHistoryAdminDetailView.as_view(), name="admin-about-history-detail"),

    # # Admin - Vision
    # path('admin/about/vision', AboutVisionAdminView.as_view(), name="admin-about-vision"),
    # path('admin/about/vision/<int:id>', AboutVisionAdminDetailView.as_view(), name="admin-about-vision-detail"),

    # # Admin - Differentiators
    # path('admin/about/differentiators', AboutDifferentiatorsAdminView.as_view(), name="admin-about-differentiators"),
    # path('admin/about/differentiators/<int:id>', AboutDifferentiatorsAdminDetailView.as_view(), name="admin-about-differentiators-detail"),

    # # Admin - Team
    # path('admin/about/team', AboutTeamAdminView.as_view(), name="admin-about-team"),
    # path('admin/about/team/<int:id>', AboutTeamAdminDetailView.as_view(), name="admin-about-team-detail"),
]