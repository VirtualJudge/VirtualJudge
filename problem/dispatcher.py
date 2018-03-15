from problem.models import Problem
from problem.models import ProblemBuilder
from VirtualJudgeSpider.Control import Controller
from utils.request import ProblemRequest
from problem.models import ProblemBuilder


class ProblemException(Exception):
    def __init__(self, err="Get Problem Failed"):
        Exception.__init__(self, err)


class ProblemDispatchar(object):
    def __init__(self, problem_id):
        self.problem = Problem.objects.get(id=problem_id)

    def submit(self):
        if self.problem.retry_count > 3:
            self.problem.request_status = ProblemRequest.status['ERROR']
            self.problem.save()
            return
        self.problem.retry_count = self.problem.retry_count + 1
        self.problem.request_status = ProblemRequest.status['CRAWLING']
        self.problem.save()
        try:
            problem_data = Controller.get_problem(self.problem.remote_oj, self.problem.remote_id).get_dict()
            self.problem = ProblemBuilder.update_problem(self.problem, problem_data)
            self.problem.request_status = ProblemRequest.status['SUCCESS']
            self.problem.save()
        except Exception as e:
            raise ProblemException
