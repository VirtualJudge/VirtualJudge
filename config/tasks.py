from celery import shared_task
from config.models import RemoteLanguage
from config.models import RemoteAccount
from VirtualJudgeSpider import Control, Config


@shared_task
def update_remote_language_task():
    RemoteLanguage.objects.all().delete()
    for remote_oj in Control.Controller.get_supports():
        remote_oj_accounts = RemoteAccount.objects.filter(oj_name=remote_oj)
        if remote_oj_accounts is not None:
            account = Config.Account(remote_oj_accounts[0].oj_username, remote_oj_accounts[0].oj_password)
            languages = Control.Controller.find_language(remote_oj, account)
            print(languages)
            if languages:
                remote_languages = []
                for k, v in languages.items():
                    remote_languages.append(
                        RemoteLanguage(oj_language=k, oj_language_name=v, oj_name=remote_oj))
                RemoteLanguage.objects.bulk_create(remote_languages)
