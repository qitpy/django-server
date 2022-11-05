from django.db import models
import re
import random
import string

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    '''Manager for user'''

    def random_verify_email_code(self):
        verify_email_code = ''.join(random.choice(string.ascii_letters) for i in range(20))
        return verify_email_code;

    def create_user(self, email, name, password=None):
        '''create, save and return a new user'''
        if not email:
            raise ValueError('User must have an email address')
        if not name:
            raise ValueError('User must have a name')
        if not password:
            raise ValueError('User must have a password')

        if not re.fullmatch('^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,32}', password):
            raise ValueError('Password must be have at least ' \
                + 'one normal character, ' \
                + 'one uppercase characters ' \
                + 'and one number')

        verify_email_code = self.random_verify_email_code()

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            verify_email_code=verify_email_code,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        '''create and return a new superuser'''
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''User in the system'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=False, unique=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    password_attempt_times = models.IntegerField(default=0)
    verify_email_code = models.CharField(max_length=255, null=True)
    verify_start_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email