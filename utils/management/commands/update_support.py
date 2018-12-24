from django.core.management.base import BaseCommand
from spider.core import Core

from support.models import Support

from support.tasks import update_oj_status


class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Core.get_supports():
            if not Support.objects.filter(oj_name=item):
                Support.objects.create(oj_name=item).save()
                update_oj_status.delay(item)
