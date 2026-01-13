from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)


class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
            user_type=User.UserType.SUPERADMIN
        )
        return user
    
    
    
class User(AbstractBaseUser, PermissionsMixin):

    class UserType(models.TextChoices):
        SUPERADMIN = "superadmin"
        TENANT_ADMIN = "tenant_admin"
        TENANT_EDITOR = "tenant_editor"
        WEB_USER = "web_user"   # futuro OAuth

    email = models.EmailField(unique=True)

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices
    )

    tenant = models.ForeignKey(
        "core.Tenant",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="users"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
