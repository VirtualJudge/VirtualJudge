from django.db import transaction
from config.models import SettingOJ
from django.core.exceptions import ObjectDoesNotExist


class ConfigDispatcher(object):
    @staticmethod
    def choose_config(key, value):
        if transaction.atomic():
            try:
                setting = SettingOJ.objects.get(oj_key=key)
                if setting.oj_value != value:
                    setting.oj_value = value
                    setting.save()
                    return True
            except ObjectDoesNotExist:
                setting = SettingOJ.objects.create(oj_key=key, oj_value=value)
                setting.save()
                return True
        return False

    @staticmethod
    def release_config(key,value):
        with transaction.atomic():
            setting = SettingOJ.objects.get(oj_key=key)
            setting.oj_value = value
            setting.save()
            print('release config')
