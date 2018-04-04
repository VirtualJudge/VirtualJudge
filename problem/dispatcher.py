from VirtualJudgeSpider.Control import Controller

from config.dispatcher import ConfigDispatcher
from problem.models import ProblemBuilder
from utils.request import ProblemRequest


class ProblemDispatchar(object):
    def __init__(self, problem):
        self.problem = problem

    def submit(self):
        account = ConfigDispatcher.choose_account(self.problem['remote_oj'])
        if not account:
            print('account all locked')
            return False
        try:
            response = Controller.get_problem(self.problem['remote_oj'], self.problem['remote_id'], account=account)
            if response:
                problem_data = response.get_dict()
                self.problem = ProblemBuilder.build_problem(problem_data)
                self.problem.request_status = ProblemRequest.status['SUCCESS']
                self.problem.save()
                ConfigDispatcher.release_account(account.id)
                return True
            ConfigDispatcher.release_account(account.id)
            return False
        except:
            ConfigDispatcher.release_account(account.id)
            return False
