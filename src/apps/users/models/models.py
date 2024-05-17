import uuid

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models.managers import UserManager


class User(auth_models.AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(_("email address"), unique=True)

    username = None

    objects = UserManager()
