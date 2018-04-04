import os

from VirtualJudgeStorage.Control import LocalStorage
from celery import shared_task
import time
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
