from VirtualJudgeSpider import Control
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.views import View

from problem.models import Problem
from problem.serializers import ProblemSerializer, ProblemListSerializer
from problem.tasks import get_problem_task
from utils.request import ProblemStatus
from utils.response import *

"""
通过数据库中的id获取题目
-----------------------------
    @:param: 
        id: 数据库中的编号
"""


class ProblemLocalAPI(View):
    def get(self, *args, **kwargs):
        try:
            problem = Problem.objects.get(id=kwargs['problem_id'])
            return JsonResponse(success(ProblemSerializer(problem).data))
        except ObjectDoesNotExist:
            pass
        return JsonResponse(error('problem not found'))


"""
通过源OJ的名称和源OJ的题目编号获取题目
---------------------------
    @:param
        remote_oj: 源OJ名称
        remote_id: 源OJ题目编号
        force_update: 强制更新
"""


class ProblemRemoteAPI(View):
    force_update = False

    def get(self, *args, **kwargs):

        remote_oj = Control.Controller.get_real_remote_oj(kwargs['remote_oj'])
        remote_id = kwargs['remote_id']
        if not Control.Controller.is_support(remote_oj) or not remote_id.isalnum():
            return HttpResponse('remote_oj or remote_id not valid')

        try:
            problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
            if problem.request_status == ProblemStatus.STATUS_NETWORK_ERROR.value:
                get_problem_task.delay(problem.id)
        except ObjectDoesNotExist:
            problem = Problem(remote_oj=remote_oj, remote_id=remote_id,
                              request_status=ProblemStatus.STATUS_PENDING.value)
            problem.save()
            get_problem_task.delay(problem.id)
        except ValueError:
            return HttpResponse('ValueError')

        if problem.request_status == ProblemStatus.STATUS_CRAWLING_SUCCESS.value:
            return JsonResponse(success(ProblemSerializer(problem).data))
        elif problem.request_status == ProblemStatus.STATUS_PROBLEM_NOT_EXIST.value:
            return JsonResponse(info({'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'NOT FOUND'}))
        else:
            return JsonResponse(error({'remote_oj': remote_oj, 'remote_id': remote_id, 'status': 'CRAWLING'}))


"""
获取题目列表
—————————————————————————————————————
@:param
    offset: 偏移
    limit: 限制
"""


class ProblemListAPI(View):
    def get(self, *args, **kwargs):
        offset = 0
        limit = 20
        for k, v in kwargs.items():
            if k == 'offset':
                offset = v
            if k == 'limit':
                limit = v
        problems = Problem.objects.filter(request_status=ProblemStatus.STATUS_CRAWLING_SUCCESS.value).order_by('-id')[
                   offset:offset + limit]
        return JsonResponse(ProblemListSerializer(problems, many=True).data, safe=False)
