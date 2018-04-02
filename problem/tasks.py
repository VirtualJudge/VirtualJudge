import os
import time

from VirtualJudgeStorage.Control import LocalStorage
from celery import shared_task, Task

from problem.dispatcher import ProblemDispatchar, ProblemException


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


@shared_task
def save_files(oj_name, pid, storage_files):
    try:
        base_path = '/public'
        dir_path = os.path.join(base_path, oj_name, pid)
        os.mkdir(dir_path)
        for storage_file in storage_files:
            LocalStorage.save_file(dir_path, storage_file.url, storage_file.file_name)
    except:
        pass
