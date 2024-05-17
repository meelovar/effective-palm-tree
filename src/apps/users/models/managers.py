from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            error_message = "The given email must be set"

            raise ValueError(error_message)

        extra_fields.setdefault("is_active", False)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.password = make_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            error_message = "Superuser must have is_staff=True."

            raise ValueError(error_message)

        if extra_fields.get("is_superuser") is not True:
            error_message = "Superuser must have is_superuser=True."

            raise ValueError(error_message)

        return self.create_user(email, password, **extra_fields)
