import os
import time
import traceback

import requests
from spider import core, config, utils
from bs4 import BeautifulSoup
from celery import shared_task
from django.db import DatabaseError
from django.db.models import F
from ws.client import SimpleWsClient
from VirtualJudge import settings
from user.models import UserProfile
from problem.models import Problem
from submission.models import Submission
from submission.serializers import VerdictSerializer


def load_static(remote_oj, remote_id, website_data):
    soup = BeautifulSoup(website_data, 'lxml')
    id = 1
    for img in soup.find_all('img'):
        url = img['src']

        file_name_list = str(url).split('/')[-1].split('.')

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
            if len(file_name_list) > 1 and file_name_list[-1].isalpha():
                file_name = f'IMG_{str(id)}.{file_name_list[-1]}'
            else:
                file_name = f'IMG_{str(id)}'
            with open(os.path.join(path, file_name), 'wb') as fout:
                fout.write(res.content)
            img['src'] = os.path.join(url_path, file_name)
            id += 1
        except OSError:
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


@shared_task
def reload_result_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        sleep_time = 3
        retry_times = 40
        while sleep_time > 0:
            result = core.Core(submission.remote_oj).get_result_by_rid_and_pid(rid=submission.unique_key,
                                                                               pid=submission.remote_id)
            if result.status == config.Result.Status.STATUS_RESULT_SUCCESS:
                submission.verdict = result.verdict.value
                submission.unique_key = result.unique_key
                submission.verdict_info = result.verdict_info
                submission.execute_time = result.execute_time
                submission.execute_memory = result.execute_memory
                SimpleWsClient('submission', str(submission.id),
                               {'verdict': submission.verdict,
                                'execute_memory': submission.execute_memory,
                                'execute_time': submission.execute_time,
                                'verdict_info': submission.verdict_info})
                if submission.verdict != config.Result.Verdict.VERDICT_RUNNING.value:
                    submission.save()
                    hook_task.delay(submission.id)
                    UserProfile.objects.filter(username=submission.user).update(hook_times=F('hook_times') + 1)
                    break
                submission.save()
            time.sleep(sleep_time)
            retry_times -= 1
        submission.reloadable = True
        submission.save()
    except DatabaseError:
        pass


@shared_task
def hook_task(submission_id):
    try:
        if len(Submission.objects.filter(id=submission_id)):
            submission = Submission.objects.get(id=submission_id)
            user_profile = UserProfile.objects.get(username=submission.user)
            if user_profile.hook is not None:
                req = utils.HttpUtil()
                req.post(url=user_profile.hook, json=VerdictSerializer(submission).data)
            submission.hook = True
            submission.save()
            user_profile.hook_times += 1
            user_profile.save()
    except DatabaseError:
        pass
