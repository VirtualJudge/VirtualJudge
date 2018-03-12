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
        "FAILED": 3,
    }


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
        account = self.choose_account(self.submission.remote_oj)
        if not account:
            pass
        submit_result = Controller.submit_code(self.submission.remote_oj,
                                               Account(username=account.oj_username, password=account.oj_password),
                                               self.submission.code,
                                               self.submission.language,
                                               self.submission.remote_id)
        if submit_result:
            self.submission.verdict = "Accepted"
            result = Controller.get_result(self.submission.remote_oj,
                                           Account(username=account.oj_username, password=account.oj_password),
                                           self.submission.remote_id)
            if not result:
                pass
            if Controller.is_waiting_for_judge(self.submission.remote_oj, result):
                pass
            self.submission.status = JudgeStatus.status['SUCCESS']
            self.submission.save()
        else:
            self.submission.status = JudgeStatus.status['FAILED']
            self.submission.save()
        self.release_account(account.id)
