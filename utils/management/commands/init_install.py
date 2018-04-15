import os

from django.core.management.base import BaseCommand
from django.db import connection
import traceback
from VirtualJudge.utils import get_env
from django.db.utils import OperationalError


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            connection.cursor()
        except OperationalError:
            self.stdout.write(self.style.WARNING('waiting database connect'))
            exit(1)
        if os.system('python3 manage.py init_database') != 0:
            self.stdout.write(self.style.ERROR('failed execute:python3 manage.py init_database'))
            exit(1)
        self.stdout.write(self.style.SUCCESS("python3 manage.py init_database:Done"))
        if os.system('python3 manage.py init_user') != 0:
            self.stdout.write(self.style.ERROR('failed execute:python3 manage.py init_user'))
            exit(1)
        self.stdout.write(self.style.SUCCESS("python3 manage.py init_user:Done"))

        if get_env('VJ_ENV', 'develop') == 'production' and os.system(
                'python3 manage.py collectstatic --noinput') != 0:
            self.stdout.write(self.style.ERROR('failed execute:python3 manage.py collectstatic'))
            exit(1)
        self.stdout.write(self.style.SUCCESS("python3 manage.py collectstatic --noinput:Done"))
