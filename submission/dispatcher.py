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
        remote_account = ConfigDispatcher.choose_account(self._submission.remote_oj)
        if remote_account is None:
            self._submission.status = Config.Result.Status.STATUS_NO_ACCOUNT.value
            self._submission.save()
            return False
        account = Config.Account(remote_account.oj_username, remote_account.oj_password)
        tries = 3
        submit_code = False
        while tries > 0 and submit_code is False:
            submit_code = Control.Controller(self._submission.remote_oj).submit_code(self._submission.remote_id,
                                                                                     account,
                                                                                     self._submission.code,
                                                                                     self._submission.language)

            tries -= 1
        if submit_code is False:
            self._submission.status = Config.Result.Status.STATUS_NETWORK_ERROR.value
            self._submission.save()
            ConfigDispatcher.release_account(remote_account.id)
            return False
        result = Control.Controller(self._submission.remote_oj).get_result(pid=self._submission.remote_id,
                                                                           account=account)
        if result.status == Config.Result.Status.STATUS_RESULT_GET:
            self._submission.status = result.status.value
            self._submission.remote_run_id = result.origin_run_id
            self._submission.execute_time = result.execute_time
            self._submission.execute_memory = result.execute_memory
            self._submission.verdict = result.verdict
            self._submission.save()
            reload_result_task.delay(self._submission.id)
            ConfigDispatcher.release_account(remote_account.id)
            return True
        else:
            self._submission.status = Config.Result.Status.STATUS_NETWORK_ERROR.value
            self._submission.save()
            ConfigDispatcher.release_account(remote_account.id)
            return False
