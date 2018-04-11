from VirtualJudgeSpider import Control, Config
from VirtualJudgeSpider.Control import Controller
from celery import shared_task

from remote.dispatcher import ConfigDispatcher
from remote.models import Account
from remote.models import Language


@shared_task
def update_remote_language_task():
    if ConfigDispatcher.choose_config('UPDATE_CONFIG', 'TRUE'):
        try:
            remote_languages = Language.objects.all()
            remote_languages.delete()
            for remote_oj in Control.Controller.get_supports():
                remote_oj_accounts = Account.objects.filter(oj_name=remote_oj)
                if len(remote_oj_accounts):
                    account = Config.Account(remote_oj_accounts[0].oj_username, remote_oj_accounts[0].oj_password)
                    languages = Controller(remote_oj).find_language(account)
                    if languages:
                        remote_languages = []
                        for k, v in languages.items():
                            remote_languages.append(
                                Language(oj_language=k, oj_language_name=v, oj_name=remote_oj))
                        Language.objects.bulk_create(remote_languages)
        except:
            import traceback
            traceback.print_exc()
        ConfigDispatcher.release_config('UPDATE_CONFIG', 'FALSE')
