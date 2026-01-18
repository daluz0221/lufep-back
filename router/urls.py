
from django.urls import path, include

urlpatterns = [
    path('api/cms', include("cms.urls")),
    
]