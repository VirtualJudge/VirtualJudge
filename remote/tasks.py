from celery import shared_task
from django.db.models import Count
from VirtualJudgeSpider import Control, Config
from remote.dispatcher import ConfigDispatcher
from remote.models import Account
from remote.models import Language
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError


@shared_task
def update_language_task():
    if ConfigDispatcher.choose_config('UPDATE_CONFIG', 'TRUE'):
        try:
            remote_languages = Language.objects.all()
            remote_languages.delete()
            for remote_oj in Account.objects.values('oj_name').annotate(rcount=Count('oj_name')):

                account = ConfigDispatcher.choose_account(remote_oj.get('oj_name'))
                if account is None:
                    continue
                langs = Control.Controller(remote_oj.get('oj_name')).find_language(
                    account=Config.Account(username=account.oj_username, password=account.oj_password))
                ConfigDispatcher.release_account(account.id)
                if langs is None:
                    continue
                for lang, lang_name in langs.items():
                    try:
                        language = Language.objects.get(oj_name=remote_oj.get('oj_name'), oj_language=lang)
                        language.oj_language_name = lang_name
                        language.save()
                    except ObjectDoesNotExist:
                        language = Language(oj_name=remote_oj.get('oj_name'), oj_language=lang,
                                            oj_language_name=lang_name)
                        language.save()
                    except DatabaseError:
                        pass
        except DatabaseError:
            import traceback
            traceback.print_exc()
        ConfigDispatcher.release_config('UPDATE_CONFIG', 'FALSE')
