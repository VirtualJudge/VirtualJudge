import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if os.system('python3 manage.py makemigrations') != 0:
            self.stdout.write(self.style.ERROR('python3 manage.py makemigrations'))
            exit(1)
        if os.system('python3 manage.py makemigrations user') != 0:
            self.stdout.write(self.style.ERROR('python3 manage.py makemigrations user'))
            exit(1)
        if os.system('python3 manage.py makemigrations support') != 0:
            self.stdout.write(self.style.ERROR('python3 manage.py makemigrations support'))
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
