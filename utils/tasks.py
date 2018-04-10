import os
import traceback

import requests
from bs4 import BeautifulSoup
from celery import shared_task

from VirtualJudge import settings
from problem.models import Problem


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
def save_files_task(local_pid):
    try:
        problem = Problem.objects.get(id=local_pid)
        if problem.html:
            problem.html = load_static(problem.remote_oj, problem.remote_id, problem.html)
            problem.save()
    except:
        traceback.print_exc()
        pass
