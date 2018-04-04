from VirtualJudgeSpider.Control import Controller
from django.db import transaction

from config.models import RemoteAccount
from problem.models import Problem
from problem.models import ProblemBuilder
from utils.request import ProblemRequest


class ProblemException(Exception):
    def __init__(self, err="Get Problem Failed"):
        Exception.__init__(self, err)


class ProblemDispatchar(object):
    def __init__(self, problem_id):
        self.problem = Problem.objects.get(id=problem_id)

    @staticmethod
    def choose_account(remote_oj):
        with transaction.atomic():
            remote_accounts = RemoteAccount.objects.filter(oj_name=remote_oj, oj_account_status=True)
            if remote_accounts:
                remote_account = remote_accounts[0]
                remote_account.oj_account_status = False
                remote_account.save()
                print('lock account:' + str(remote_account.oj_name) + ' ' + str(remote_account.oj_username))
                return remote_account
        return None

    @staticmethod
    def release_account(remote_account_id):
        with transaction.atomic():
            remote_account = RemoteAccount.objects.get(id=remote_account_id)
            remote_account.oj_account_status = True
            remote_account.save()

    def submit(self):
        if self.problem.retry_count > 3:
            self.problem.request_status = ProblemRequest.status['ERROR']
            self.problem.save()
            return
        account = self.choose_account(self.problem.remote_oj)
        if not account:
            self.problem.retry_count = self.problem.retry_count + 1
            self.problem.request_status = ProblemRequest.status['CRAWLING']
            self.problem.save()
            raise ProblemException

        try:
            response = Controller.get_problem(self.problem.remote_oj, self.problem.remote_id, account=account)
            if response:
                problem_data = response.get_dict()
                self.problem = ProblemBuilder.update_problem(self.problem, problem_data)
                self.problem.request_status = ProblemRequest.status['SUCCESS']
                self.problem.save()
        except:
            self.release_account(account.id)
            raise ProblemException
        self.release_account(account.id)
