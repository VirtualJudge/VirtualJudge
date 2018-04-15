from VirtualJudgeSpider import Control, Config
from celery import shared_task
from django.db import DatabaseError

from remote.dispatcher import ConfigDispatcher
from remote.models import Language


@shared_task
def update_language_task(remote_oj):
    if ConfigDispatcher.choose_config('UPDATE_LANGUAGE_' + str(remote_oj).upper(), 'TRUE'):

        r_account = ConfigDispatcher.choose_account(remote_oj)
        if r_account is None:
            ConfigDispatcher.release_config('UPDATE_LANGUAGE_' + str(remote_oj).upper(), 'FALSE')
            return
        langs = Control.Controller(remote_oj).find_language(
            account=Config.Account(username=r_account.oj_username, password=r_account.oj_password))
        ConfigDispatcher.release_account(r_account.id)

        if langs is None:
            ConfigDispatcher.release_config('UPDATE_LANGUAGE_' + str(remote_oj).upper(), 'FALSE')
            return
        Language.objects.filter(oj_name=remote_oj).delete()
        for lang, lang_name in langs.items():
            try:
                language = Language(oj_name=remote_oj, oj_language=lang, oj_language_name=lang_name)
                language.save()
            except DatabaseError:
                pass
        ConfigDispatcher.release_config('UPDATE_LANGUAGE_' + str(remote_oj).upper(), 'FALSE')
