from VirtualJudgeSpider import Control, Config
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from problem.models import Problem
from problem.tasks import get_problem_task
from utils.response import *


@require_GET
def check_status(request):
    return HttpResponse('Virtual Judge Status Success\n')


def get_problem(request, remote_oj, remote_id):
    if not Control.Controller.is_support(remote_oj) or not remote_id.isalnum():
        return HttpResponse('remote_oj or remote_id not valid')
    remote_oj = Control.Controller.get_real_remote_oj(remote_oj)
    try:
        problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
        if problem.request_status in [Config.Problem.Status.STATUS_NETWORK_ERROR.value,
                                      Config.Problem.Status.STATUS_NO_ACCOUNT.value]:
            get_problem_task.delay(problem.id)
    except ObjectDoesNotExist:
        problem = Problem(remote_oj=remote_oj, remote_id=remote_id,
                          request_status=Config.Problem.Status.STATUS_PENDING.value)
        problem.save()
        get_problem_task.delay(problem.id)
    except ValueError:
        return HttpResponse('ValueError')

    if problem.request_status == Config.Problem.Status.STATUS_CRAWLING_SUCCESS.value:
        return render(request, 'problem.html', {'problem': problem.__dict__})
    elif problem.request_status == Config.Problem.Status.STATUS_PROBLEM_NOT_EXIST.value:
        return render(request, 'problem-error.html',
                      {'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'PROBLEM NOT FOUND'})
    elif problem.request_status == Config.Problem.Status.STATUS_NETWORK_ERROR.value:
        return render(request, 'problem-error.html',
                      {'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'NETWORK ERROR'})
    elif problem.request_status == Config.Problem.Status.STATUS_PARSE_ERROR.value:
        return render(request, 'problem-error.html',
                      {'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'PARSE ERROR'})
    elif problem.request_status == Config.Problem.Status.STATUS_OJ_NOT_EXIST.value:
        return render(request, 'problem-error.html',
                      {'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'OJ NOT FOUND'})
    elif problem.request_status == Config.Problem.Status.STATUS_NO_ACCOUNT.value:
        return render(request, 'problem-error.html',
                      {'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'NO ACCOUNT'})
    else:
        return render(request, 'problem-error.html',
                      {'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'CRAWLING'})


def get_problem_html(request, remote_oj, remote_id):
    if not Control.Controller.is_support(remote_oj) or not remote_id.isalnum():
        return HttpResponse(None)
    remote_oj = Control.Controller.get_real_remote_oj(remote_oj)
    try:
        problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
        if problem.request_status == Config.Problem.Status.STATUS_CRAWLING_SUCCESS.value:
            return HttpResponse(problem.html)
        elif problem.request_status == Config.Problem.Status.STATUS_RUNING.value:
            return JsonResponse(success('Crawling from remote...'))
        else:
            return JsonResponse(error('Get remote problem error'))
    except:
        return HttpResponse('ERROR')
