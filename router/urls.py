
from django.urls import path, include #type: ignore

urlpatterns = [
    path('api/v1/cms/', include("cms.urls")),
    path('api/v1/auth/', include("core.urls"))
]