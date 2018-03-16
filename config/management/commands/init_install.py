from django.core.management.base import BaseCommand, CommandError
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            if os.system('python3 manage.py init_database') != 0:
                self.stdout.write(self.style.ERROR('failed execute:python3 manage.py init_database'))
                exit(1)
            # if os.system('python3 manage.py init_remote') != 0:
            #     self.stdout.write(self.style.ERROR('failed execute:python3 manage.py init_remote'))
            #     exit(1)
            # self.stdout.write(self.style.SUCCESS("Done"))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Failed to initialize, error: ' + str(e)))
