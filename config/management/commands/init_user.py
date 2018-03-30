from django.core.management.base import BaseCommand, CommandError
import os
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            try:
                User.objects.get(username='root')
            except ObjectDoesNotExist:
                user = User.objects.create('root', 'root@vj.com', 'rootroot')
                user.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to create user, error: ' + str(e)))
            exit(1)
