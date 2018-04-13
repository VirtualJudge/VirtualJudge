from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from account.models import UserProfile
from django.db import DatabaseError


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = 'root'
        email = 'root@vj.com'
        password = 'rootroot'
        try:
            user = UserProfile.objects.create_superuser(username=username, email=email, password=password)
            user.save()
        except DatabaseError:
            self.stdout.write(self.style.WARNING('we did not create new root account, maybe account exist.'))
        try:
            UserProfile.objects.get(username=username)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR('Failed to create user'))
            exit(1)
