import time
from problem.models import Problem
from celery import shared_task
from utils.request import ProblemStatus
from problem.dispatcher import ProblemDispatchar


@shared_task
def get_problem_task(problem_id):
    try:
        problem = Problem.objects.get(id=problem_id)
        if problem.request_status in [ProblemStatus.STATUS_PENDING.value,
                                      ProblemStatus.STATUS_NETWORK_ERROR.value,
                                      ProblemStatus.STATUS_CRAWLING_SUCCESS.value]:
            problem.request_status = ProblemStatus.STATUS_RUNING.value
            problem.save()
        max_tries = 4
        now = 0
        while now < max_tries:
            try:
                ProblemDispatchar(problem_id).submit()
                problem = Problem.objects.get(id=problem_id)
                if problem.request_status in [ProblemStatus.STATUS_RUNING.value,
                                              ProblemStatus.STATUS_PROBLEM_NOT_EXIST.value,
                                              ProblemStatus.STATUS_CRAWLING_SUCCESS.value]:
                    break
            except:
                break
            now += 1
            time.sleep(2)
    except:
        pass
