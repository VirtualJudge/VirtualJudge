from celery import shared_task
from django.db import DatabaseError
from spider import config
from spider.core import Core

from support.dispatcher import ConfigDispatcher
from support.models import Language
from support.models import Support


@shared_task
def update_oj_status(oj_name):
    try:
        oj = Support.objects.get(oj_name=oj_name)
        print(oj_name, Core(oj_name=oj_name, proxies=oj.oj_proxies).check_status())
        oj.oj_status = 'SUCCESS' if Core(oj_name=oj_name, proxies=oj.oj_proxies).check_status() else 'FAILED'
        oj.save()
    except:
        pass


@shared_task
def update_language_task(remote_oj):
    if ConfigDispatcher.choose_config('UPDATE_LANGUAGE_' + str(remote_oj).upper(), 'TRUE'):

        account = ConfigDispatcher.choose_account(remote_oj)
        if account is None:
            ConfigDispatcher.release_config('UPDATE_LANGUAGE_' + str(remote_oj).upper(), 'FALSE')
            return
        remote_account = config.Account(username=account.oj_username, password=account.oj_password,
                                        cookies=account.cookies)
        core = Core(remote_oj)
        langs = core.find_language(account=remote_account)
        print(remote_oj, langs)
        try:
            account.cookies = core.get_cookies()
            account.save()
        except Exception as e:
            print(e)
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
