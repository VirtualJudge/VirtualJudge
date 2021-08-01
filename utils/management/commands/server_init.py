import os
import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError

from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        tries = 5
        wait_secs = 4
        while True:
            try:
                connection.cursor()
                self.stdout.write(self.style.SUCCESS('Database connected.'))
                break
            except OperationalError:
                self.stdout.write(self.style.WARNING('Waiting database connect.'))
                tries -= 1
                if tries <= 0:
                    break
                time.sleep(wait_secs)

        if os.system('python manage.py makemigrations') != 0:
            self.stdout.write(self.style.ERROR('Make migrations error.'))
            exit(1)
        self.stdout.write(self.style.SUCCESS("Make migrations success."))
        if os.system('python manage.py migrate') != 0:
            self.stdout.write(self.style.ERROR('Migrate error.'))
            exit(1)
        self.stdout.write(self.style.SUCCESS("Migrate success."))

        username = 'banana'
        email = 'banana@vj.com'
        password = 'banana1234'
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING('Due to the existence of this user, no new super user was created.'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)

        self.stdout.write(self.style.SUCCESS("Create super user success."))
