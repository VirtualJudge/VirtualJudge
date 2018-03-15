from VirtualJudgeSpider.Config import Account
from VirtualJudgeSpider.Control import Controller
from django.db import transaction

from config.models import RemoteAccount
from submission.models import Submission
from utils.request import JudgeRequest


class SubmissionException(Exception):
    def __init__(self, err='Submission Error'):
        Exception.__init__(self, err)


class SpiderDispatcher(object):
    def __init__(self, submission_id):
        self.submission = Submission.objects.get(id=submission_id)
        self.remote_account = None

    @staticmethod
    def choose_account(remote_oj):
        with transaction.atomic():
            remote_accounts = RemoteAccount.objects.filter(oj_name=remote_oj, oj_account_status=True)
            if remote_accounts:
                remote_account = remote_accounts[0]
                remote_account.oj_account_status = False
                remote_account.save()
                return remote_account
        return None

    @staticmethod
    def release_account(remote_account_id):
        with transaction.atomic():
            remote_account = RemoteAccount.objects.get(id=remote_account_id)
            remote_account.oj_account_status = True
            remote_account.save()

    def submit(self):
        if self.submission.retry_count > 10:
            return
        if self.submission.status == JudgeRequest.status['PENDING'] or \
                self.submission.status == JudgeRequest.status['SEND_FOR_JUDGE_ERROR']:
            account = self.choose_account(self.submission.remote_oj)
            if not account:
                self.submission.retry_count = self.submission.retry_count + 1
                self.submission.save()
                raise SubmissionException
            success_submit = Controller.submit_code(self.submission.remote_oj,
                                                    Account(username=account.oj_username, password=account.oj_password),
                                                    self.submission.code,
                                                    self.submission.language,
                                                    self.submission.remote_id)
            if success_submit:
                result = Controller.get_result(self.submission.remote_oj,
                                               Account(username=account.oj_username, password=account.oj_password),
                                               self.submission.remote_id)
                if not result:
                    if self.submission.status == JudgeRequest.status['SEND_FOR_JUDGE_ERROR']:
                        self.submission.status = JudgeRequest.status['RETRY']
                    else:
                        self.submission.status = JudgeRequest.status['SEND_FOR_JUDGE_ERROR']
                    self.release_account(account.id)
                    self.submission.retry_count = self.submission.retry_count + 1
                    self.submission.save()
                    raise Submission

                self.submission.remote_run_id = result.origin_run_id
                self.submission.verdict = result.verdict
                self.submission.execute_memory = result.execute_memory
                self.submission.execute_time = result.execute_time
                if Controller.is_waiting_for_judge(self.submission.remote_oj, result.verdict):
                    self.submission.status = JudgeRequest.status['JUDGING']
                    self.submission.retry_count = self.submission.retry_count + 1
                    self.submission.save()
                    self.release_account(account.id)
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
                self.release_account(account.id)
                raise SubmissionException
            self.release_account(account.id)
        elif self.submission.status == JudgeRequest.status['JUDGING']:
            result = Controller.get_result_by_rid(self.submission.remote_oj, self.submission.remote_run_id)
            if Controller.is_waiting_for_judge(self.submission.remote_oj, result.verdict):
                self.submission.status = JudgeRequest.status['JUDGING']
                self.submission.retry_count = self.submission.retry_count + 1
                self.submission.save()
                raise SubmissionException

            self.submission.verdict = result.verdict
            self.submission.execute_memory = result.execute_memory
            self.submission.execute_time = result.execute_time
            self.submission.status = JudgeRequest.status['SUCCESS']
            self.submission.save()
