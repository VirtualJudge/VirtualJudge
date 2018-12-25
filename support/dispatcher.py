from django.db import DatabaseError
from django.db import transaction
from django.utils import timezone

from support.models import Setting, Account


class ConfigDispatcher(object):
    @staticmethod
    def choose_config(key, value):
        if transaction.atomic():
            try:
                if Setting.objects.filter(oj_key=key).exists():
                    setting = Setting.objects.get(oj_key=key)

                    if (setting.update_time - timezone.now()).seconds > 5 and setting.oj_value != value:
                        setting.oj_value = value
                        setting.save()
                        return True
                    else:
                        return False
                else:
                    setting = Setting(oj_key=key, oj_value=value)
                    setting.save()
                    return True
            except DatabaseError:
                return False
        return False

    @staticmethod
    def release_config(key, value):
        with transaction.atomic():
            Setting.objects.filter(oj_key=key).update(oj_value=value)

    @staticmethod
    def choose_account(remote_oj):
        with transaction.atomic():
            remote_accounts = Account.objects.filter(oj_name=remote_oj,
                                                     status=True).order_by('update_time')
            if remote_accounts and (timezone.now() - remote_accounts[0].update_time).seconds >= 5:
                remote_account = remote_accounts[0]
                remote_account.status = False
                remote_account.save()
                print(remote_account.oj_username)
                return remote_account
        return None

    @staticmethod
    def release_account(remote_account_id):
        with transaction.atomic():
            remote_account = Account.objects.get(id=remote_account_id)
            remote_account.status = True
            remote_account.save()
