from django.core.management.base import BaseCommand, CommandError
import os
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            user = User.objects.create_superuser('root', 'root@vj.com', 'rootroot')
            user.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to create user, error: ' + str(e)))
            exit(1)
