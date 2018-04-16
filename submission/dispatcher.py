from VirtualJudgeSpider import Control, Config
from django.core.exceptions import ObjectDoesNotExist

from remote.dispatcher import ConfigDispatcher
from submission.models import Submission
from utils.tasks import reload_result_task


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
            self._submission.status = Config.Result.Status.STATUS_NO_ACCOUNT.value
            self._submission.save()
            return False
        remote_account = Config.Account(account.oj_username, account.oj_password, account.cookies)

        controller = Control.Controller(self._submission.remote_oj)
        submit_code = controller.submit_code(self._submission.remote_id, remote_account, self._submission.code,
                                             self._submission.language)
        account.cookies = controller.get_cookies()
        account.save()
        if submit_code is False:
            self._submission.status = Config.Result.Status.STATUS_NETWORK_ERROR.value
            self._submission.save()
            ConfigDispatcher.release_account(account.id)
            return False

        result = controller.get_result(pid=self._submission.remote_id, account=remote_account)
        account.cookies = controller.get_cookies()
        account.save()

        if result.status == Config.Result.Status.STATUS_RESULT:
            self._submission.status = result.status.value
            self._submission.remote_run_id = result.origin_run_id
            self._submission.execute_time = result.execute_time
            self._submission.execute_memory = result.execute_memory
            self._submission.verdict = result.verdict
            self._submission.verdict_code = result.verdict_code.value
            self._submission.save()
            reload_result_task.delay(self._submission.id)
            ConfigDispatcher.release_account(account.id)
            return True
        else:
            self._submission.status = Config.Result.Status.STATUS_NETWORK_ERROR.value
            self._submission.verdict_code = result.verdict_code.value
            self._submission.save()
            ConfigDispatcher.release_account(account.id)
            return False
