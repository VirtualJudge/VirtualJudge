from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from spider.config import Problem as Spider_Problem

from problem.models import Problem
from problem.serializers import ProblemSerializer, ProblemListSerializer
from problem.tasks import get_problem_task
from support.models import Support
from utils.response import res_format, Message


class ProblemHtmlAPI(APIView):
    def get(self, request, remote_oj, remote_id, **kwargs):

        try:
            problem = Problem.objects.get(remote_oj=remote_oj,
                                          remote_id=remote_id)
            if problem.request_status in [Spider_Problem.Status.STATUS_SUBMIT_FAILED.value,
                                          Spider_Problem.Status.STATUS_PROBLEM_NOT_EXIST.value,
                                          Spider_Problem.Status.STATUS_NO_ACCOUNT.value,
                                          Spider_Problem.Status.STATUS_PARSE_ERROR.value]:
                problem.request_status = Spider_Problem.Status.STATUS_PENDING.value
                problem.save()
                get_problem_task.delay(problem.id)
        except ObjectDoesNotExist:
            problem = Problem(remote_oj=remote_oj, remote_id=remote_id,
                              request_status=Spider_Problem.Status.STATUS_PENDING.value)
            problem.save()
            get_problem_task.delay(problem.id)
        return HttpResponse(problem.html)


class ProblemAPI(APIView):
    def get(self, request, remote_oj, remote_id, **kwargs):
        if remote_oj not in list({item.oj_name for item in Support.objects.filter(oj_enable=True)}):
            return Response(
                res_format('remote_oj not valid', status=Message.ERROR),
                status=status.HTTP_200_OK)
        if not remote_id.isalnum():
            return Response(
                res_format('remote_id not valid', status=Message.ERROR),
                status=status.HTTP_200_OK)
        if request.GET.get('fresh') and request.GET.get('html'):
            return Response(res_format('\"fresh\" and \"html\" cannot exist together', Message.ERROR),
                            status=status.HTTP_200_OK)
        if request.GET.get('fresh'):
            last_submit_time = request.session.get('last_fresh_time', None)
            if last_submit_time and (datetime.now() - datetime.fromtimestamp(last_submit_time)).seconds < 5:
                return Response(res_format("Cannot fresh within five seconds", status=Message.ERROR),
                                status=status.HTTP_200_OK)
            request.session['last_fresh_time'] = datetime.now().timestamp()
            try:
                problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
                problem.request_status = Spider_Problem.Status.STATUS_PENDING.value
                problem.save()
                get_problem_task.delay(problem.id)
                return Response(res_format(ProblemSerializer(problem).data), status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(res_format('System error', Message.ERROR), status=status.HTTP_200_OK)

        if request.GET.get('html'):
            try:
                problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
                return HttpResponse(problem.html)
            except:
                return Response(res_format('', status=Message.ERROR))
        try:
            problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
            if problem.request_status in [Spider_Problem.Status.STATUS_SUBMIT_FAILED.value,
                                          Spider_Problem.Status.STATUS_PROBLEM_NOT_EXIST.value,
                                          Spider_Problem.Status.STATUS_NO_ACCOUNT.value,
                                          Spider_Problem.Status.STATUS_PARSE_ERROR.value]:
                get_problem_task.delay(problem.id)
        except ObjectDoesNotExist:
            try:
                problem = Problem(remote_oj=remote_oj, remote_id=remote_id,
                                  request_status=Spider_Problem.Status.STATUS_PENDING.value)
                problem.save()
                get_problem_task.delay(problem.id)
            except IntegrityError:
                return Response(res_format('System error', Message.ERROR), status=status.HTTP_200_OK)
        return Response(res_format(ProblemSerializer(problem).data), status=status.HTTP_200_OK)


class ProblemFreshAPI(APIView):
    def get(self, request, remote_oj, remote_id, **kwargs):
        pass


class ProblemListAPI(APIView):
    def get(self, request, *args, **kwargs):
        problems = Problem.objects.filter(
            Q(remote_oj__in=[item.oj_name for item in Support.objects.filter(oj_enable=True)]) & Q(
                html__isnull=False)).order_by('-update_time')
        if request.GET.get('remote_oj'):
            remote_oj = request.GET.get('remote_oj')
            problems = problems.filter(remote_oj=remote_oj)
        if request.GET.get('remote_id'):
            problems = problems.filter(remote_id__contains=request.GET.get('remote_id'))
        if request.GET.get('title'):
            problems = problems.filter(title__contains=request.GET.get('title'))
        return Response(res_format(ProblemListSerializer(problems, many=True).data), status=status.HTTP_200_OK)
