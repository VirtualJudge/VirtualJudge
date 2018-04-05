from VirtualJudgeSpider.Control import Controller

from config.dispatcher import ConfigDispatcher
from problem.models import ProblemBuilder, Problem
from utils.request import ProblemRequest
import traceback
from django.core.exceptions import ObjectDoesNotExist


class ProblemDispatchar(object):
    def __init__(self, problem):
        self.problem = problem

    def submit(self):
        account = ConfigDispatcher.choose_account(self.problem['remote_oj'])
        if not account:
            print('account all locked')
            return False
        try:
            ret = None
            try:
                ret = Problem.objects.get(remote_oj=self.problem['remote_oj'], remote_id=self.problem['remote_id'])
            except ObjectDoesNotExist:
                ret = Problem(remote_oj=self.problem['remote_oj'], remote_id=self.problem['remote_id'],request_status=ProblemRequest.status['ERROR'])
                ret.save()
            response = Controller.get_problem(self.problem['remote_oj'], self.problem['remote_id'], account=account)
            if response:
                problem_data = response.get_dict()
                if ret:
                    problem_obj = ProblemBuilder.update_problem(ret, problem_data)
                    problem_obj.request_status = ProblemRequest.status['SUCCESS']
                    problem_obj.save()
                else:
                    problem_obj = ProblemBuilder.build_problem(problem_data)
                    problem_obj.request_status = ProblemRequest.status['SUCCESS']
                    problem_obj.save()
                ConfigDispatcher.release_account(account.id)
                return True
            ConfigDispatcher.release_account(account.id)
            return False
        except:
            traceback.print_exc()

            ConfigDispatcher.release_account(account.id)
            return False
