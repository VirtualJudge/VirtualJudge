from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET
from django.views import View
from problem.models import Problem, ProblemBuilder
from problem.serializers import ProblemSerializer, ProblemListSerializer
from problem.utils import *
from problem.tasks import get_problem_task

"""
通过数据库中的id获取题目
-----------------------------
    @:param: 
        id: 数据库中的编号
"""


class ProblemLocalAPI(View):
    def get(self, problem_id):
        try:
            problem = Problem.objects.get(id=problem_id)
            return JsonResponse(ProblemSerializer(problem).data)
        except ObjectDoesNotExist:
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
获取数据库中题目总数
------------------------------------
@:param
    None
"""


@require_GET
def get_problem_count(request):
    return Problem.objects.all().count()


"""
获取题目列表
—————————————————————————————————————
@:param
    offset: 偏移
    limit: 限制
"""


def get_problem_list(request, offset=0, limit=20):
    problems = Problem.objects.all().order_by('-id')[offset:offset + limit]
    return JsonResponse(ProblemListSerializer(problems, many=True).data, safe=False)
