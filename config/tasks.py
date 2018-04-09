from VirtualJudgeSpider import Control, Config
from VirtualJudgeSpider.Control import Controller
from celery import shared_task

from config.dispatcher import ConfigDispatcher
from config.models import RemoteAccount
from config.models import RemoteLanguage


@shared_task
def update_remote_language_task():
    if ConfigDispatcher.choose_config('UPDATE_CONFIG', 'TRUE'):
        try:
            remote_languages = RemoteLanguage.objects.all()
            remote_languages.delete()
            for remote_oj in Control.Controller.get_supports():
                remote_oj_accounts = RemoteAccount.objects.filter(oj_name=remote_oj)
                if len(remote_oj_accounts):
                    account = Config.Account(remote_oj_accounts[0].oj_username, remote_oj_accounts[0].oj_password)
                    languages = Controller(remote_oj).find_language(account)
                    if languages:
                        remote_languages = []
                        for k, v in languages.items():
                            remote_languages.append(
                                RemoteLanguage(oj_language=k, oj_language_name=v, oj_name=remote_oj))
                        RemoteLanguage.objects.bulk_create(remote_languages)
        except:
            import traceback
            traceback.print_exc()
        ConfigDispatcher.release_config('UPDATE_CONFIG', 'FALSE')
