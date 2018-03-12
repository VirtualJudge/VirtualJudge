from django.core.management.base import BaseCommand
import os
from VirtualJudgeSpider import Control
from VirtualJudgeSpider.Config import Account
from config.models import RemoteOJ, RemoteAccount, RemoteLanguage
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            RemoteAccount.objects.all().delete()
            RemoteLanguage.objects.all().delete()
            RemoteOJ.objects.all().delete()
        except Exception as e:
            self.stdout.write(self.style.ERROR('failed to clean remote online judge config database'))
            exit(1)

        for oj_name in Control.support_ojs:
            remote_oj = RemoteOJ()
            remote_oj.oj_name = oj_name
            remote_oj.oj_status = Control.Controller.check_status(oj_name)
            remote_oj.save()
        try:
            account_url = '/Users/prefixai/workspace/accounts.json'
            with open(account_url, 'r') as fin:
                data = fin.read().encode('utf-8')
                oj_accounts = json.loads(data)
                for oj_account in oj_accounts:
                    RemoteAccount(oj_name=oj_account['remote_oj'], oj_username=oj_account['username'],
                                  oj_password=oj_account['password']).save()
        except Exception as e:
            self.stdout.write(self.style.ERROR('failed create remote account:' + str(e)))
            exit(1)

        try:
            remote_ojs = RemoteOJ.objects.all()
            for remote_oj in remote_ojs:
                remote_oj_accounts = RemoteAccount.objects.filter(oj_name=remote_oj.oj_name)
                if remote_oj_accounts is not None:
                    account = Account(remote_oj_accounts[0].oj_username, remote_oj_accounts[0].oj_password)
                    languages = Control.Controller.find_language(remote_oj.oj_name, account)
                    if languages:
                        for k, v in languages.items():
                            RemoteLanguage(oj_language=k, oj_language_name=v, oj_name=remote_oj.oj_name).save()
        except Exception as e:
            self.stdout.write(self.style.ERROR('failed create remote language:' + str(e)))
            exit(1)
