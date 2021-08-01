import os

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError

from vj.utils import get_env


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            connection.cursor()
        except OperationalError:
            self.stdout.write(self.style.WARNING('waiting database connect'))
            exit(1)
        if os.system('python3 manage.py migrate') != 0:
            self.stdout.write(self.style.ERROR('python3 manage.py migrate'))
            exit(1)
        self.stdout.write(self.style.SUCCESS("python3 manage.py migrate:Done"))
        if os.system('python3 manage.py init_user') != 0:
            self.stdout.write(self.style.ERROR('failed execute:python3 manage.py init_user'))
            exit(1)
        self.stdout.write(self.style.SUCCESS("python3 manage.py init_user:Done"))

        if get_env('VJ_ENV', 'develop') == 'production' and os.system(
                'python3 manage.py collectstatic --noinput') != 0:
            self.stdout.write(self.style.ERROR('failed execute:python3 manage.py collectstatic'))
            exit(1)
        self.stdout.write(self.style.SUCCESS("python3 manage.py collectstatic --noinput:Done"))
