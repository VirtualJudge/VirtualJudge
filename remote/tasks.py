from VirtualJudgeSpider import control, config
from celery import shared_task
from django.db import DatabaseError

from remote.dispatcher import ConfigDispatcher
from remote.models import Language


@shared_task
def update_language_task(remote_oj):
    print(remote_oj)
    if ConfigDispatcher.choose_config('UPDATE_LANGUAGE_' + str(remote_oj).upper(), 'TRUE'):

        account = ConfigDispatcher.choose_account(remote_oj)
        if account is None:
            ConfigDispatcher.release_config('UPDATE_LANGUAGE_' + str(remote_oj).upper(), 'FALSE')
            return
        remote_account = config.Account(username=account.oj_username, password=account.oj_password,
                                        cookies=account.cookies)
        controller = control.Controller(remote_oj)
        langs = controller.find_language(account=remote_account)
        print(remote_oj, langs)
        account.cookies = controller.get_cookies()
        account.save()
        ConfigDispatcher.release_account(account.id)

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
