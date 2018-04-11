from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from account.models import UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            try:
                UserProfile.objects.get(username='root')
            except ObjectDoesNotExist:
                user = UserProfile.objects.create_superuser('root', 'root@vj.com', 'rootroot')
                user.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to create user, error: ' + str(e)))
            exit(1)
