''''
Django command to wait for the database to be available
'''
import time

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    '''Django command to create superuser'''

    def handle(self, *args, **option):
        '''create new superuser'''
        phone_number = input('phone_number: ')
        email = input('email: ')
        name = input('name: ')
        password = None
        password_confirm = None
        while password is None or password_confirm != password:

            password = input('password: ')
            password_confirm = input('confirm password: ')

        user = get_user_model().objects.create_superuser(
            phone_number, email, name, password
        )

        # notify that command is successful
        self.stdout.write(self.style.SUCCESS('💪' + name + 'created!'))