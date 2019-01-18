from django.core.exceptions import ObjectDoesNotExist
from spider.config import Account, Result
from spider.core import Core
from ws.client import SimpleWsClient
from submission.models import Submission
from support.dispatcher import ConfigDispatcher
from utils.tasks import reload_result_task, hook_task


class SubmissionDispatcher(object):
    def __init__(self, submission_id):
        try:
            self._submission = Submission.objects.get(id=submission_id)
        except ObjectDoesNotExist:
            self._submission = None
        self.remote_account = None

    def submit(self):
        if self._submission is None:
            return False
        account = ConfigDispatcher.choose_account(self._submission.remote_oj)
        if account is None:
            self._submission.status = Result.Status.STATUS_SPIDER_ERROR.value
            self._submission.save()
            return False
        remote_account = Account(account.oj_username, account.oj_password, account.cookies)

        core = Core(self._submission.remote_oj)
        result = core.submit_code(account=remote_account, pid=self._submission.remote_id,
                                  language=self._submission.language, code=self._submission.code)
        try:
            account.cookies = core.get_cookies()
            account.save()
        except:
            pass

        if result.status == Result.Status.STATUS_RESULT_SUCCESS:
            self._submission.status = result.status.value
            self._submission.unique_key = result.unique_key
            self._submission.execute_time = result.execute_time
            self._submission.execute_memory = result.execute_memory
            self._submission.verdict = result.verdict.value
            self._submission.verdict_info = result.verdict_info
            self._submission.save()
            SimpleWsClient('submission',
                           {'verdict': self._submission.verdict,
                            'id': self._submission.id,
                            'execute_memory': self._submission.execute_memory,
                            'execute_time': self._submission.execute_time,
                            'verdict_info': self._submission.verdict_info}).execute()
            if self._submission.verdict == Result.Verdict.VERDICT_RUNNING.value:
                reload_result_task.delay(self._submission.id)
            else:
                self._submission.reloadable = True
                self._submission.save()
                hook_task.delay(self._submission.id)
            ConfigDispatcher.release_account(account.id)
            return True
        else:
            self._submission.status = Result.Status.STATUS_SUBMIT_ERROR.value
            self._submission.save()
            ConfigDispatcher.release_account(account.id)
            return False
