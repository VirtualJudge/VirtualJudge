import time
import traceback

from VirtualJudgeSpider import Config
from celery import shared_task

from problem.dispatcher import ProblemDispatcher
from problem.models import Problem


@shared_task
def get_problem_task(problem_id):
    problem = Problem.objects.get(id=problem_id)
    if problem.request_status in [Config.Problem.Status.STATUS_PENDING.value,
                                  Config.Problem.Status.STATUS_NETWORK_ERROR.value,
                                  Config.Problem.Status.STATUS_PROBLEM_NOT_EXIST.value,
                                  Config.Problem.Status.STATUS_NO_ACCOUNT.value,
                                  Config.Problem.Status.STATUS_CRAWLING_SUCCESS.value]:
        problem.request_status = Config.Problem.Status.STATUS_RUNNING.value
        problem.save()
    tries = 4

    while tries > 0 and ProblemDispatcher(problem_id).submit():
        tries -= 1
        time.sleep(2)
