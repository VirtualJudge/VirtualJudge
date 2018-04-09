from VirtualJudgeSpider.Config import Account
from VirtualJudgeSpider.Control import Controller

from config.dispatcher import ConfigDispatcher
from submission.models import Submission
from utils.request import JudgeRequest


class SubmissionException(Exception):
    def __init__(self, err='Submission Error'):
        Exception.__init__(self, err)


class SubmissionDispatcher(object):
    def __init__(self, submission_id):
        self.submission = Submission.objects.get(id=submission_id)
        self.remote_account = None

    def submit(self):
        if self.submission.retry_count > 10:
            return
        if self.submission.status == JudgeRequest.status['PENDING'] or \
                self.submission.status == JudgeRequest.status['SEND_FOR_JUDGE_ERROR']:
            account = ConfigDispatcher.choose_account(self.submission.remote_oj)
            if not account:
                self.submission.retry_count = self.submission.retry_count + 1
                self.submission.save()
                raise SubmissionException
            success_submit = Controller(self.submission.remote_oj).submit_code(
                account=Account(username=account.oj_username, password=account.oj_password),
                code=self.submission.code,
                language=self.submission.language,
                pid=self.submission.remote_id)
            if success_submit:
                result = Controller(self.submission.remote_oj, ).get_result(
                    account=Account(username=account.oj_username, password=account.oj_password),
                    pid=self.submission.remote_id)
                if not result:
                    if self.submission.status == JudgeRequest.status['SEND_FOR_JUDGE_ERROR']:
                        self.submission.status = JudgeRequest.status['RETRY']
                    else:
                        self.submission.status = JudgeRequest.status['SEND_FOR_JUDGE_ERROR']
                    ConfigDispatcher.release_account(account.id)
                    self.submission.retry_count = self.submission.retry_count + 1
                    self.submission.save()
                    raise Submission

                self.submission.remote_run_id = result.origin_run_id
                self.submission.verdict = result.verdict
                self.submission.execute_memory = result.execute_memory
                self.submission.execute_time = result.execute_time
                if Controller(self.submission.remote_oj).is_waiting_for_judge(result.verdict):
                    self.submission.status = JudgeRequest.status['JUDGING']
                    self.submission.retry_count = self.submission.retry_count + 1
                    self.submission.save()
                    ConfigDispatcher.release_account(account.id)
                    raise SubmissionException
                self.submission.status = JudgeRequest.status['SUCCESS']
                self.submission.save()
            else:
                if self.submission.status == JudgeRequest.status['SEND_FOR_JUDGE_ERROR']:
                    self.submission.status = JudgeRequest.status['RETRY']
                else:
                    self.submission.status = JudgeRequest.status['SEND_FOR_JUDGE_ERROR']
                self.submission.retry_count = self.submission.retry_count + 1
                self.submission.save()
                ConfigDispatcher.release_account(account.id)
                raise SubmissionException
            ConfigDispatcher.release_account(account.id)
        elif self.submission.status == JudgeRequest.status['JUDGING']:
            result = Controller(self.submission.remote_oj).get_result_by_rid_and_pid(self.submission.remote_run_id,
                                                                                     self.submission.remote_id)
            if Controller(self.submission.remote_oj).is_waiting_for_judge(result.verdict):
                self.submission.status = JudgeRequest.status['JUDGING']
                self.submission.retry_count = self.submission.retry_count + 1
                self.submission.save()
                raise SubmissionException

            self.submission.verdict = result.verdict
            self.submission.execute_memory = result.execute_memory
            self.submission.execute_time = result.execute_time
            self.submission.status = JudgeRequest.status['SUCCESS']
            self.submission.save()
