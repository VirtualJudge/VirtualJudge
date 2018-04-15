from VirtualJudgeSpider import Control
from VirtualJudgeSpider.Config import Problem as Spider_Problem
from django.core.exceptions import ObjectDoesNotExist

from problem.models import ProblemBuilder, Problem
from remote.dispatcher import ConfigDispatcher
from utils.tasks import save_files_task


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
        response = Control.Controller(self.problem.remote_oj).get_problem(
            self.problem.remote_id, account=account)
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
