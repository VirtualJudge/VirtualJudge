import os
import traceback

import requests
from bs4 import BeautifulSoup
from celery import shared_task

from VirtualJudge import settings
from problem.models import Problem
from submission.models import Submission
from VirtualJudgeSpider import Control, Config
import time


def load_static(remote_oj, remote_id, website_data):
    soup = BeautifulSoup(website_data, 'lxml')
    for img in soup.find_all('img'):
        url = img['src']
        file_name = str(url).split('/')[-1]
        path = settings.PUBLIC_DIR
        path = os.path.join(path, remote_oj)
        path = os.path.join(path, remote_id)
        url_path = settings.PUBLIC
        url_path = os.path.join(url_path, remote_oj)
        url_path = os.path.join(url_path, remote_id)

        res = requests.get(url)
        if res.status_code != 200:
            continue
        try:
            os.makedirs(path)
        except:
            pass
        img['src'] = os.path.join(url_path, file_name)
        with open(os.path.join(path, file_name), 'wb') as fout:
            fout.write(res.content)
    return str(soup)


@shared_task
def save_files_task(problem_id):
    try:
        problem = Problem.objects.get(id=problem_id)
        if problem.html:
            problem.html = load_static(problem.remote_oj, problem.remote_id, problem.html)
            problem.save()
    except:
        traceback.print_exc()
        pass


@shared_task
def reload_result_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        tries = 5
        max_wait_times = 5
        while tries > 0 and Control.Controller(submission.remote_oj).is_waiting_for_judge(submission.verdict):
            result = Control.Controller(submission.remote_oj).get_result_by_rid_and_pid(rid=submission.remote_run_id,
                                                                                        pid=submission.remote_id)
            if result.status == Config.Result.Status.STATUS_RESULT_GET:
                submission.verdict = result.verdict
                if not Control.Controller(submission.remote_oj).is_waiting_for_judge(submission.verdict):
                    submission.verdict_status = True
                submission.execute_time = result.execute_time
                submission.execute_memory = result.execute_memory
                submission.save()
            tries -= 1
            time.sleep(max_wait_times - tries)
    except:
        traceback.print_exc()
        pass
