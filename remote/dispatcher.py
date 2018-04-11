from django.db import transaction
from remote.models import Setting, Account
from django.core.exceptions import ObjectDoesNotExist
from VirtualJudgeSpider.Control import Controller
from django.utils import timezone


class ConfigDispatcher(object):
    @staticmethod
    def choose_config(key, value):
        if transaction.atomic():
            try:
                setting = Setting.objects.get(oj_key=key)
                if setting.oj_value != value:
                    setting.oj_value = value
                    setting.save()
                    print('LOCK remote')
                    return True
            except ObjectDoesNotExist:
                try:
                    setting = Setting.objects.create(oj_key=key, oj_value=value)
                    setting.save()
                    print('LOCK remote')
                    return True
                except:
                    return False

        return False

    @staticmethod
    def release_config(key, value):
        with transaction.atomic():
            setting = Setting.objects.get(oj_key=key)
            setting.oj_value = value
            setting.save()
            print('RELEASE remote')

    @staticmethod
    def choose_account(remote_oj):
        with transaction.atomic():
            remote_accounts = Account.objects.filter(oj_name=Controller.get_real_remote_oj(remote_oj),
                                                     oj_account_status=True).order_by('update_time')
            if remote_accounts and (timezone.now() - remote_accounts[0].update_time).seconds >= 5:
                remote_account = remote_accounts[0]
                remote_account.oj_account_status = False
                remote_account.save()
                print('LOCK account:' + str(remote_account.oj_name) + ':' + remote_account.oj_username)
                return remote_account
        return None

    @staticmethod
    def release_account(remote_account_id):
        with transaction.atomic():
            remote_account = Account.objects.get(id=remote_account_id)
            remote_account.oj_account_status = True
            remote_account.save()
            print('RELEASE account:' + str(remote_account.oj_name) + ':' + remote_account.oj_username)
