from django.db import transaction
from config.models import SettingOJ, RemoteAccount
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
    def release_config(key, value):
        with transaction.atomic():
            setting = SettingOJ.objects.get(oj_key=key)
            setting.oj_value = value
            setting.save()
            print('release config')

    @staticmethod
    def choose_account(remote_oj):
        with transaction.atomic():
            remote_accounts = RemoteAccount.objects.filter(oj_name=remote_oj, oj_account_status=True)
            if remote_accounts:
                remote_account = remote_accounts[0]
                remote_account.oj_account_status = False
                remote_account.save()
                return remote_account
        return None

    @staticmethod
    def release_account(remote_account_id):
        with transaction.atomic():
            remote_account = RemoteAccount.objects.get(id=remote_account_id)
            remote_account.oj_account_status = True
            remote_account.save()
