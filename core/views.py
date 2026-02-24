from typing import Any

from django.contrib.auth import authenticate # type: ignore
from django.contrib.auth.models import AnonymousUser # type: ignore
from django.contrib.auth.password_validation import validate_password # type: ignore

from rest_framework import status # type: ignore
from rest_framework.request import Request # type: ignore
from rest_framework.permissions import IsAuthenticated, BasePermission # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore

from .models.website import Website
from .models.user import User
from .services.throttles import LoginRateThrottle


class PasswordChangedPermission(BasePermission):

    def has_permission(self, request, view: any) -> bool:# type: ignore[override]
        user = request.user

        # Si no está autenticado, DRF lo bloquea antes
        if not user.is_authenticated:
            return False

        return not user.must_change_password

class AdminView(APIView):
    permission_classes = [IsAuthenticated, PasswordChangedPermission] 
    
   


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
        if user.must_change_password:
            return Response({
                "must_change_password": True,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
    
        
        
        domains = Website.objects.filter(
            tenant=user.tenant
        ).values("id", "domains")
        
        return Response({
            "must_change_password": False,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "domains": list(domains)
        }, status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    

    
    def post(self, request):
        
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = authenticate(username=email, password=password)
        if not isinstance(user, User):
            return Response({"Error": "Invalidad credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get("new_password")
        
        
        validate_password(new_password, user)
        
        user.set_password(new_password)
        user.must_change_password = False
        user.save()
        
        return Response(
            {"message": "contraseña actualizada"},
            status=status.HTTP_200_OK
        )