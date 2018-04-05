import time

from celery import shared_task

from problem.dispatcher import ProblemDispatchar


@shared_task
def get_problem_task(problem):
    max_tries = 4
    now = 0
    while now < max_tries:
        if ProblemDispatchar(problem).submit():
            break
        now += 1
        time.sleep(2)



