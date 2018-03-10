from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_GET

from problem.forms import GetProblemByRemoteInfoForm, GetProblemListForm, GetProblemByIdForm
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
def get_problem_by_id(request):
    form = GetProblemByIdForm(request.GET)
    if form.is_valid():
        id = form.cleaned_data['id']
        problem = None
        try:
            problem = Problem.objects.get(id=id)
        except ObjectDoesNotExist:
            pass
        return JsonResponse(ProblemSerializer(problem).data)
    return HttpResponseNotFound('404')


"""
通过源OJ的名称和源OJ的题目编号获取题目
---------------------------
    @:param
        remote_oj: 源OJ名称
        remote_id: 源OJ题目编号
"""


@require_GET
def get_problem_by_roj_and_rid(request):
    form = GetProblemByRemoteInfoForm(request.GET)
    if form.is_valid():
        remote_oj = form.cleaned_data['remote_oj'].strip()
        remote_id = form.cleaned_data['remote_id'].strip()
        force_update = form.cleaned_data['force_update']
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

    return HttpResponseNotFound('404')


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
    page_number: 页号
    page_size: 页大小
"""


@require_GET
def get_problem_list(request):
    form = GetProblemListForm(request.GET)
    if form.is_valid():
        page_number = form.cleaned_data['page_number']
        page_size = form.cleaned_data['page_size']
        problems = Problem.objects.all().order_by('-id')[(page_number - 1) * page_size:page_number * page_size]
        return JsonResponse(ProblemListSerializer(problems, many=True).data, safe=False)
    return HttpResponseNotFound('404')
