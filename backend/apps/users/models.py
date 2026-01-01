from django.db import models
from uuid6 import uuid7
from core.models import UUIDModel, TimeStampedModel, StatusModel
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid7
    )
    email = models.EmailField(unique=True)
    # invalid_try = models.IntegerField(default=0)
    # otp = models.CharField(max_length=8, blank=True, null=True)
    # otp_valid_until = models.DateTimeField(null=True)
    # is_banned = models.BooleanField(default=False)
    # banned_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class UserProfile(UUIDModel):
    birth_date = models.DateTimeField()
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"