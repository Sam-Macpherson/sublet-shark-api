from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import gettext_lazy as _

from subletshark import settings
from subletshark.storage_backends import PublicImageStorage


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


def image_filename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_id/filename
    return f'user_{instance.id}/{instance.profile_picture.name}'


def select_storage():
    return PublicImageStorage() if settings.USE_S3 else FileSystemStorage()


class User(AbstractUser):
    """Custom user model for sublet shark."""
    username = None
    email = models.EmailField('Email Address', unique=True)
    profile_picture = models.ImageField(
        null=True, blank=True,
        storage=select_storage,
        upload_to=image_filename,
    )
    bio = models.TextField(
        null=True, blank=True,
        max_length=512,
        help_text=_('A short bio for a user of the platform to describe their situation.')
    )
    STATUS_NONE = 10
    STATUS_SEARCHING = 20
    STATUS_OFFERING = 30
    STATUS_CHOICES = (
        (STATUS_NONE, 'None'),
        (STATUS_SEARCHING, 'Searching'),
        (STATUS_OFFERING, 'Offering'),
    )
    sublet_status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_NONE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
