from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    '''Manager for user'''
    def create_user(self, phone_number, email, name, password=None):
        '''create, save and return a new user'''
        if not phone_number:
            raise ValueError('User must have an phone number')
        if not email:
            raise ValueError('User must have an email address')
        if not name:
            raise ValueError('User must have a name')

        print('======', phone_number, '======')

        user = self.model(
            phone_number=phone_number,
            email=email,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, email, name, password=None):
        '''create and return a new superuser'''
        user = self.create_user(phone_number, email, name, password)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''User in the system'''
    phone_number = PhoneNumberField(region='VN', unique=True, max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=False, unique=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'