import os
import time
import traceback

import requests
from VirtualJudgeSpider import control, config
from bs4 import BeautifulSoup
from celery import shared_task
from django.db import DatabaseError

from VirtualJudge import settings
from problem.models import Problem
from submission.models import Submission


def load_static(remote_oj, remote_id, website_data):
    soup = BeautifulSoup(website_data, 'lxml')
    id = 1
    for img in soup.find_all('img'):
        url = img['src']

        suffix = str(url).split('/')[-1].split('.')[-1]
        path = settings.PUBLIC_DIR
        path = os.path.join(path, remote_oj)
        path = os.path.join(path, remote_id)
        url_path = settings.PUBLIC_URL
        url_path = os.path.join(url_path, remote_oj)
        url_path = os.path.join(url_path, remote_id)

        res = requests.get(url)
        if res.status_code != 200:
            continue
        try:
            if os.path.exists(path) is False:
                os.makedirs(path)
            file_name = str(id) + '.' + suffix
            with open(os.path.join(path, file_name), 'wb') as fout:
                fout.write(res.content)
            img['src'] = os.path.join(url_path, file_name)
            id += 1
        except OSError:
            traceback.print_exc()
            pass
    return str(soup)


@shared_task
def save_files_task(problem_id):
    try:
        problem = Problem.objects.get(id=problem_id)
        if problem.html:
            problem.html = load_static(problem.remote_oj, problem.remote_id, problem.html)
            problem.save()
    except DatabaseError:
        traceback.print_exc()
        pass


@shared_task
def reload_result_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        if control.Controller(submission.remote_oj).is_running(submission.verdict) is False:
            submission.verdict_status = 0
            submission.save()
        else:
            tries = 5
            max_wait_times = 5
            while tries > 0:
                result = control.Controller(submission.remote_oj).get_result_by_rid_and_pid(
                    rid=submission.remote_run_id,
                    pid=submission.remote_id)
                if result.status == config.Result.Status.STATUS_RESULT:
                    submission.verdict = result.verdict
                    submission.verdict_code = result.verdict_code.value
                    submission.execute_time = result.execute_time
                    submission.execute_memory = result.execute_memory
                    if control.Controller(submission.remote_oj).is_running(submission.verdict) is False:
                        submission.verdict_status = True
                        submission.save()
                        break
                    submission.save()
                tries -= 1
                time.sleep(max_wait_times - tries)
    except DatabaseError:
        import traceback
        traceback.print_exc()
