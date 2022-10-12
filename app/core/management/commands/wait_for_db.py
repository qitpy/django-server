'''
Django command to wait for the database to be available
'''
import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for the database"""

    def handle(self, *args, **options):
        '''Entrypoint for command'''
        self.stdout.write('👋 waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write(
                    self.style.NOTICE(
                        '💩 Database unavailable, waiting for 1 second...'
                    )
                )
                time.sleep(1)

        # notify that command is successful
        self.stdout.write(self.style.SUCCESS('Database available!'))
