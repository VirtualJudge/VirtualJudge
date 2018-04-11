from django.core.management.base import BaseCommand, CommandError
import os
from VirtualJudge.utils import get_env


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
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
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to initialize, error: ' + str(e)))
