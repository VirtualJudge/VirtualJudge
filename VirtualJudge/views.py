from django.http import HttpResponse
from django.views.decorators.http import require_GET
from problem.models import Problem
from django.core.exceptions import ObjectDoesNotExist
from problem.tasks import get_problem_task
from django.http import JsonResponse
from VirtualJudgeSpider import Config, Control
from utils.response import *
from django.shortcuts import render


@require_GET
def check_status(request):
    return HttpResponse('Virtual Judge Status Success')


def get_problem(request, remote_oj, remote_id):
    problem = None

    remote_oj = Control.Controller.get_real_remote_oj(remote_oj)
    try:
        problem_obj = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
        return render(request, 'problem.html', {'problem': problem_obj.__dict__})
    except ObjectDoesNotExist:
        pass
    except ValueError:
        pass
    if not problem:
        problem = Config.Problem()
        problem.remote_oj = remote_oj
        problem.remote_id = remote_id
        get_problem_task.delay(problem.__dict__)
        return render(request, 'problem-error.html', {'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'crawling'})
    return render(request, 'problem-error.html', {'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'error'})


def get_problem_html(request, remote_oj, remote_id):
    problem = None

    remote_oj = Control.Controller.get_real_remote_oj(remote_oj)
    try:
        problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
        return HttpResponse(problem.html)
    except ObjectDoesNotExist:
        pass
    except ValueError:
        pass
    if not problem:
        problem = Config.Problem()
        problem.remote_oj = remote_oj
        problem.remote_id = remote_id
        print('get problem:', problem.remote_oj, problem.remote_id)
        get_problem_task.delay(problem.__dict__)
        return HttpResponse(success('Crawling From Remote....'))
    return HttpResponse(error('get remote problem error'))
