from VirtualJudgeSpider import Control, Config
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
    def get(self, request, problem_id, **kwargs):
        try:
            problem = Problem.objects.get(id=problem_id)
            return Response(res_format(ProblemSerializer(problem).data), status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(res_format('problem not exist', status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)


class ProblemAPI(APIView):
    def get(self, request, remote_oj, remote_id, **kwargs):
        remote_oj = Control.Controller.get_real_remote_oj(remote_oj)
        if not Control.Controller.is_support(remote_oj):
            return Response(res_format('remote_oj not valid', status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)
        if not remote_id.isalnum():
            return Response(res_format('remote_id not valid', status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)
        try:
            problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
            if problem.request_status in [Config.Problem.Status.STATUS_NETWORK_ERROR.value,
                                          Config.Problem.Status.STATUS_PENDING.value,
                                          Config.Problem.Status.STATUS_PROBLEM_NOT_EXIST.value,
                                          Config.Problem.Status.STATUS_NO_ACCOUNT.value,
                                          Config.Problem.Status.STATUS_CRAWLING_SUCCESS.value,
                                          Config.Problem.Status.STATUS_PARSE_ERROR.value]:
                get_problem_task.delay(problem.id)
        except ObjectDoesNotExist:
            problem = Problem(remote_oj=remote_oj, remote_id=remote_id,
                              request_status=Config.Problem.Status.STATUS_PENDING.value)
            problem.save()
            get_problem_task.delay(problem.id)
        return Response(res_format(ProblemSerializer(problem).data), status=status.HTTP_200_OK)


class ProblemListAPI(APIView):
    def get(self, request, **kwargs):
        problems = Problem.objects.filter(request_status=Config.Problem.Status.STATUS_CRAWLING_SUCCESS.value).order_by(
            '-update_time')[:100]
        return Response(res_format(ProblemListSerializer(problems, many=True).data), status=status.HTTP_200_OK)
