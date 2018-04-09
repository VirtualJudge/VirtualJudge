import traceback

from VirtualJudgeSpider.Control import Controller

from config.dispatcher import ConfigDispatcher
from problem.models import ProblemBuilder, Problem
from utils.request import ProblemStatus
from utils.tasks import save_files


class ProblemDispatchar(object):
    def __init__(self, problem_id):
        try:
            self.problem = Problem.objects.get(id=problem_id)
        except:
            traceback.print_exc()
            self.problem = None

    def submit(self):
        account = ConfigDispatcher.choose_account(self.problem.remote_oj)
        if account and self.problem:
            try:
                response = Controller(self.problem.remote_oj).get_problem(self.problem.remote_id, account=account)
                if response:
                    problem_data = response.get_dict()
                    self.problem = ProblemBuilder.update_problem(self.problem, problem_data)
                    self.problem.request_status = ProblemStatus.STATUS_CRAWLING_SUCCESS.value
                    save_files.delay(self.problem.id)
                else:
                    self.problem.request_status = ProblemStatus.STATUS_NETWORK_ERROR.value
                self.problem.save()
            except:
                traceback.print_exc()
            finally:
                ConfigDispatcher.release_account(account.id)
