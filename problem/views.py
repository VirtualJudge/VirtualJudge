from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from problem.models import Problem, ProblemBuilder
from problem.serializers import ProblemSerializer, ProblemListSerializer
from problem.utils import *

"""
通过数据库中的id获取题目
-----------------------------
    @:param: 
        id: 数据库中的编号
"""


@require_GET
def get_problem_by_id(request, problem_id):
    problem = None
    try:
        problem = Problem.objects.get(id=problem_id)
    except ObjectDoesNotExist:
        pass
    return JsonResponse(ProblemSerializer(problem).data)


"""
通过源OJ的名称和源OJ的题目编号获取题目
---------------------------
    @:param
        remote_oj: 源OJ名称
        remote_id: 源OJ题目编号
"""


@require_GET
def get_problem_by_roj_and_rid(request, remote_oj, remote_id):
    force_update = False
    problem = None
    try:
        problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
    except ObjectDoesNotExist:
        pass

    if problem is None or force_update:
        problem_data = get_problem_from_origin_online_judge(remote_oj, remote_id)
        if problem is None:
            problem = ProblemBuilder.build_problem(problem_data)
        else:
            problem = ProblemBuilder.update_problem(problem, problem_data)
        problem.save()
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


def get_problem_list(request, offset=0, limit=10):
    problems = Problem.objects.all().order_by('-id')[offset:offset + limit]
    return JsonResponse(ProblemListSerializer(problems, many=True).data, safe=False)
