from VirtualJudgeSpider.config import Problem as Spider_Problem
from VirtualJudgeSpider.control import Controller
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from problem.models import Problem
from problem.serializers import ProblemSerializer, ProblemListSerializer
from problem.tasks import get_problem_task
from utils.response import res_format, Message


class ProblemLocalAPI(APIView):
    def post(self, request, problem_id, param=None, **kwargs):
        try:
            problem = Problem.objects.get(id=problem_id)
            if param == 'html':
                return HttpResponse(problem.html)
            return Response(res_format(ProblemSerializer(problem).data),
                            status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(
                res_format('problem not exist', status=Message.ERROR),
                status=status.HTTP_200_OK)


class ProblemHtmlAPI(APIView):
    def get(self, request, remote_oj, remote_id, **kwargs):
        remote_oj = Controller.get_real_remote_oj(remote_oj)
        if not Controller.is_support(remote_oj):
            return Response(
                res_format('remote_oj not valid', status=Message.ERROR),
                status=status.HTTP_200_OK)
        if not remote_id.isalnum():
            return Response(
                res_format('remote_id not valid', status=Message.ERROR),
                status=status.HTTP_200_OK)
        try:
            problem = Problem.objects.get(remote_oj=remote_oj,
                                          remote_id=remote_id)
            if problem.request_status in [Spider_Problem.Status.STATUS_NETWORK_ERROR.value,
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
    def post(self, request, remote_oj, remote_id, **kwargs):
        remote_oj = Controller.get_real_remote_oj(remote_oj)
        if not Controller.is_support(remote_oj):
            return Response(
                res_format('remote_oj not valid', status=Message.ERROR),
                status=status.HTTP_200_OK)
        if not remote_id.isalnum():
            return Response(
                res_format('remote_id not valid', status=Message.ERROR),
                status=status.HTTP_200_OK)
        try:
            problem = Problem.objects.get(remote_oj=remote_oj,
                                          remote_id=remote_id)
            if problem.request_status in [Spider_Problem.Status.STATUS_NETWORK_ERROR.value,
                                          Spider_Problem.Status.STATUS_PROBLEM_NOT_EXIST.value,
                                          Spider_Problem.Status.STATUS_NO_ACCOUNT.value,
                                          Spider_Problem.Status.STATUS_PARSE_ERROR.value]:
                get_problem_task.delay(problem.id)
        except ObjectDoesNotExist:
            problem = Problem(remote_oj=remote_oj, remote_id=remote_id,
                              request_status=Spider_Problem.Status.STATUS_PENDING.value)
            problem.save()
            get_problem_task.delay(problem.id)
        return Response(res_format(ProblemSerializer(problem).data), status=status.HTTP_200_OK)


class ProblemListAPI(APIView):
    def post(self, request, **kwargs):
        problems = Problem.objects.filter(request_status=Spider_Problem.Status.STATUS_CRAWLING_SUCCESS.value).order_by(
            '-update_time')[:20]
        return Response(res_format(ProblemListSerializer(problems, many=True).data), status=status.HTTP_200_OK)
