from spider.core import Core
from django.core.exceptions import ObjectDoesNotExist

from problem.models import ProblemBuilder, Problem
from support.dispatcher import ConfigDispatcher
from utils.tasks import save_files_task
from spider import config


class ProblemDispatcher(object):
    def __init__(self, problem_id):
        try:
            self.problem = Problem.objects.get(id=problem_id)
        except ObjectDoesNotExist:
            self.problem = None

    def submit(self):
        if self.problem is None:
            return False
        core = Core(self.problem.remote_oj)
        account = ConfigDispatcher.choose_account(self.problem.remote_oj)
        if account is None:
            self.problem.request_status = config.Problem.Status.STATUS_RETRYABLE.value
            self.problem.save()
            return False
        remote_account = config.Account(username=account.oj_username, password=account.oj_password,
                                        cookies=account.cookies)
        response = core.get_problem(self.problem.remote_id, account=remote_account)
        try:
            account.cookies = core.get_cookies()
            account.save()
        except Exception as e:
            print(e)
        ConfigDispatcher.release_account(account.id)

        self.problem.request_status = response.status.value
        if response.status == config.Problem.Status.STATUS_SUCCESS:
            self.problem = ProblemBuilder.update_problem(self.problem, response.__dict__)
            save_files_task.delay(self.problem.id)
            self.problem.save()
            return True
        else:
            self.problem.save()
            return False
