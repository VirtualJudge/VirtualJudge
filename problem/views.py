from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View

from problem.models import Problem
from problem.serializers import ProblemSerializer, ProblemListSerializer
from problem.tasks import get_problem_task
from utils import request
from utils.decorator import token_required
from utils.response import *
from VirtualJudgeSpider import Config

"""
通过数据库中的id获取题目
-----------------------------
    @:param: 
        id: 数据库中的编号
"""


class ProblemLocalAPI(View):
    @token_required
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

    @token_required
    def get(self, *args, **kwargs):
        problem = None
        try:
            problem = Problem.objects.get(remote_oj=kwargs['remote_oj'], remote_id=kwargs['remote_id'])
            return JsonResponse(ProblemSerializer(problem).data)
        except ObjectDoesNotExist:
            pass
        if not problem or self.force_update:
            problem = Config.Problem()
            problem.remote_oj = kwargs['remote_oj']
            problem.remote_id = kwargs['remote_id']
            get_problem_task.delay(problem.__dict__)
            return JsonResponse(success('crawling from remote'))
        return JsonResponse(error('get remote problem error'))


"""
获取题目列表
—————————————————————————————————————
@:param
    offset: 偏移
    limit: 限制
"""


class ProblemListAPI(View):
    @token_required
    def get(self, *args, **kwargs):
        offset = 0
        limit = 20
        for k, v in kwargs.items():
            if k == 'offset':
                offset = v
            if k == 'limit':
                limit = v
        problems = Problem.objects.filter(request_status=request.ProblemRequest.status['SUCCESS']).order_by('-id')[
                   offset:offset + limit]
        return JsonResponse(ProblemListSerializer(problems, many=True).data, safe=False)
