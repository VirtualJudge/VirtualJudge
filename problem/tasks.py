from celery import shared_task, Task
from problem.dispatcher import ProblemDispatchar, ProblemException
import time


class ProblemTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('on_failure execute')


@shared_task(bind=Task, base=ProblemTask)
def get_problem_task(self, problem_id):
    try:
        ProblemDispatchar(problem_id).submit()
    except ProblemException as e:
        time.sleep(2)
        self.retry(exc=e)
