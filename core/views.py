

from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models.website import Website
from .models.user import User
from .services.throttles import LoginRateThrottle


class AdminView(APIView):
    permission_classes = [IsAuthenticated]


class LoginAPIView(APIView):
    
    throttle_classes = [LoginRateThrottle]
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=email, password=password)
        
        
        
        if not isinstance(user, User):
            return Response({"Error": "Invalidad credentials"}, status=status.HTTP_400_BAD_REQUEST)

    
        refresh = RefreshToken.for_user(user)
        
        domains = Website.objects.filter(
            tenant=user.tenant
        ).values("id", "domains")
        
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "domains": list(domains)
        }, status=status.HTTP_200_OK)

