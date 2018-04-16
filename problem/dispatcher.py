from VirtualJudgeSpider import Control
from VirtualJudgeSpider.Config import Problem as Spider_Problem
from django.core.exceptions import ObjectDoesNotExist

from problem.models import ProblemBuilder, Problem
from remote.dispatcher import ConfigDispatcher
from utils.tasks import save_files_task
from VirtualJudgeSpider import Config


class ProblemDispatcher(object):
    def __init__(self, problem_id):
        try:
            self.problem = Problem.objects.get(id=problem_id)
        except ObjectDoesNotExist:
            self.problem = None

    def submit(self):
        if self.problem is None:
            return False
        account = ConfigDispatcher.choose_account(self.problem.remote_oj)
        if account is None:
            self.problem.request_status = Spider_Problem.Status.STATUS_NO_ACCOUNT.value
            self.problem.save()
            return False
        remote_account = Config.Account(username=account.oj_username, password=account.oj_password,
                                        cookies=account.cookies)
        controller = Control.Controller(self.problem.remote_oj)
        response = controller.get_problem(self.problem.remote_id, account=remote_account)
        account.cookies = controller.get_cookies()
        account.save()
        ConfigDispatcher.release_account(account.id)

        self.problem.request_status = response.status.value
        if response.status == Spider_Problem.Status.STATUS_CRAWLING_SUCCESS:
            self.problem = ProblemBuilder.update_problem(self.problem, response.__dict__)
            save_files_task.delay(self.problem.id)
            self.problem.save()
            return True
        else:
            self.problem.save()
            return False
