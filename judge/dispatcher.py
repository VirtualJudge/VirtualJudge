from django.db import transaction
from submission.models import Submission
from config.models import RemoteAccount
from VirtualJudgeSpider.Control import Controller
from VirtualJudgeSpider.Config import Account, Result


class JudgeStatus:
    status = {
        "PENDING": 0,
        "JUDGING": 1,
        "SUCCESS": 2,
        "SEND_FOR_JUDGE_ERROR": 3,
        "RETRY": 4,
    }


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

        if self.submission.status == JudgeStatus.status['PENDING'] or \
                self.submission.status == JudgeStatus.status['SEND_FOR_JUDGE_ERROR']:
            account = self.choose_account(self.submission.remote_oj)
            if not account:
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
                    if self.submission.status == JudgeStatus.status['SEND_FOR_JUDGE_ERROR']:
                        self.submission.status = JudgeStatus.status['RETRY']
                    else:
                        self.submission.status = JudgeStatus.status['SEND_FOR_JUDGE_ERROR']
                    self.release_account(account.id)
                    raise Submission

                self.submission.remote_run_id = result.origin_run_id
                self.submission.verdict = result.verdict
                self.submission.execute_memory = result.execute_memory
                self.submission.execute_time = result.execute_time
                if Controller.is_waiting_for_judge(self.submission.remote_oj, result.verdict):
                    self.submission.status = JudgeStatus.status['JUDGING']
                    self.submission.save()
                    self.release_account(account.id)
                    raise SubmissionException
                self.submission.status = JudgeStatus.status['SUCCESS']
                self.submission.save()

            else:
                if self.submission.status == JudgeStatus.status['SEND_FOR_JUDGE_ERROR']:
                    self.submission.status = JudgeStatus.status['RETRY']
                else:
                    self.submission.status = JudgeStatus.status['SEND_FOR_JUDGE_ERROR']
                self.submission.save()
                self.release_account(account.id)
                raise SubmissionException

            self.release_account(account.id)
        elif self.submission.status == JudgeStatus.status['JUDGING']:
            result = Controller.get_result_by_rid(self.submission.remote_oj, self.submission.remote_run_id)
            if Controller.is_waiting_for_judge(self.submission.remote_oj, result.verdict):
                self.submission.status = JudgeStatus.status['JUDGING']
                self.submission.save()
                raise SubmissionException

            self.submission.verdict = result.verdict
            self.submission.execute_memory = result.execute_memory
            self.submission.execute_time = result.execute_time
            self.submission.status = JudgeStatus.status['SUCCESS']
            self.submission.save()
