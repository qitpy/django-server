''''
Django command to wait for the database to be available
'''
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to create superuser"""

    def handle(self, *args, **option):
        """create new superuser"""
        name = input('name: ')
        password = None
        password_confirm = None
        while password is None or password_confirm != password:
            password = input('password: ')
            password_confirm = input('confirm password: ')

        # notify that command is successful
        self.stdout.write(self.style.SUCCESS('💪' + name + 'created!'))
