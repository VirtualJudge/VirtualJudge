import os
import traceback

import requests
from VirtualJudgeSpider.Config import Desc
from celery import shared_task

from VirtualJudge import settings
from problem.models import Problem
import json


def check_json(remote_oj, remote_id, json_obj):
    if not json_obj:
        return
    for val in json_obj:
        if val['type'] in [Desc.Type.IMG, Desc.Type.PDF] and val.get('origin', None) and val.get('file_name', None):
            path = settings.PUBLIC
            path = os.path.join(path, remote_oj)
            path = os.path.join(path, remote_id)
            res = requests.get(str(val['origin']).replace('../', ''))
            if res.status_code != 200:
                continue
            try:
                os.makedirs(path)
            except:
                pass
            with open(os.path.join(os.path.abspath(path), val['file_name']), 'wb') as fout:
                fout.write(res.content)
            val['link'] = os.path.join(path, val['file_name'])


@shared_task
def save_files(local_pid):
    try:
        problem = Problem.objects.get(id=local_pid)
        check_json(problem.remote_oj, problem.remote_id, problem.description)
        check_json(problem.remote_oj, problem.remote_id, problem.input)
        check_json(problem.remote_oj, problem.remote_id, problem.output)
        check_json(problem.remote_oj, problem.remote_id, problem.author)
        check_json(problem.remote_oj, problem.remote_id, problem.source)
        check_json(problem.remote_oj, problem.remote_id, problem.hint)
        problem.save()
    except:
        traceback.print_exc()
        pass
