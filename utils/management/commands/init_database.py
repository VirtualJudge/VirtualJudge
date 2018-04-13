from django.core.management.base import BaseCommand, CommandError
import os
from VirtualJudge.settings import DATABASES


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.WARNING(DATABASES.get('default')))
            if os.system('python3 manage.py makemigrations') != 0:
                self.stdout.write(self.style.ERROR('python3 manage.py makemigrations'))
                exit(1)
            if os.system('python3 manage.py makemigrations account') != 0:
                self.stdout.write(self.style.ERROR('python3 manage.py makemigrations account'))
                exit(1)
            if os.system('python3 manage.py makemigrations remote') != 0:
                self.stdout.write(self.style.ERROR('python3 manage.py makemigrations remote'))
                exit(1)
            if os.system('python3 manage.py makemigrations problem') != 0:
                self.stdout.write(self.style.ERROR('python3 manage.py makemigrations problem'))
                exit(1)
            if os.system('python3 manage.py makemigrations submission') != 0:
                self.stdout.write(self.style.ERROR('python3 manage.py makemigrations submission'))
                exit(1)
            if os.system('python3 manage.py makemigrations contest') != 0:
                self.stdout.write(self.style.ERROR('python3 manage.py makemigrations contest'))
                exit(1)
            if os.system('python3 manage.py migrate') != 0:
                self.stdout.write(self.style.ERROR('python3 manage.py migrate'))
                exit(1)
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to initialize, error: ' + str(e)))
