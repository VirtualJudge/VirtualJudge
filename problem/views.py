from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound
from django.views import View

from problem.models import Problem
from problem.serializers import ProblemSerializer, ProblemListSerializer
from problem.tasks import get_problem_task
from utils import request

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
            return JsonResponse(ProblemSerializer(problem).data)
        except ObjectDoesNotExist:
            pass
        return HttpResponseNotFound('404')


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
        problem = None
        try:
            problem = Problem.objects.get(remote_oj=kwargs['remote_oj'], remote_id=kwargs['remote_id'])
            if self.force_update:
                problem.retry_count = 0
                problem.save()
                get_problem_task.delay(problem.id)
        except ObjectDoesNotExist:
            pass

        if problem is None:
            problem = Problem(remote_oj=kwargs['remote_oj'], remote_id=kwargs['remote_id'])
            problem.save()
            get_problem_task.delay(problem.id)
        return JsonResponse(ProblemSerializer(problem).data)


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
        problems = Problem.objects.filter(request_status=request.ProblemRequest.status['SUCCESS']).order_by('-id')[
                   offset:offset + limit]
        return JsonResponse(ProblemListSerializer(problems, many=True).data, safe=False)
