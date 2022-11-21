from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    """Manager for user"""

    def create_user(self, email, name):
        """create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address')
        if not name:
            raise ValueError('User must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        """create and return a new superuser"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=False, unique=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
