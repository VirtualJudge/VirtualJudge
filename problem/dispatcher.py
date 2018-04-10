import traceback

from config.dispatcher import ConfigDispatcher
from problem.models import ProblemBuilder, Problem
from utils.tasks import save_files_task
from VirtualJudgeSpider import Config, Control


class ProblemDispatchar(object):
    def __init__(self, problem_id):
        try:
            self.problem = Problem.objects.get(id=problem_id)
        except:
            traceback.print_exc()
            self.problem = None

    def submit(self):
        account = ConfigDispatcher.choose_account(self.problem.remote_oj)
        if type(self.problem) == Problem:
            if account:
                try:
                    response = Control.Controller(self.problem.remote_oj).get_problem(self.problem.remote_id,
                                                                                      account=account)
                    if response.status == Config.Problem.Status.STATUS_CRAWLING_SUCCESS:
                        problem_data = response.__dict__
                        self.problem = ProblemBuilder.update_problem(self.problem, problem_data)
                        self.problem.request_status = Config.Problem.Status.STATUS_CRAWLING_SUCCESS.value
                        self.problem.save()
                        save_files_task.delay(self.problem.id)
                    else:
                        self.problem.request_status = response.status.value
                        self.problem.save()
                except:
                    traceback.print_exc()
                finally:
                    ConfigDispatcher.release_account(account.id)
            else:
                self.problem.request_status = Config.Problem.Status.STATUS_NO_ACCOUNT.value
                self.problem.save()
