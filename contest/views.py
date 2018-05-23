from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response

from utils.response import res_format, Message
from .models import Contest, ContestProblem
from .serializers import ContestSerializer, ContestListSerializer, ContestProblemSerializer
from django.db import DatabaseError
from submission.models import Submission
from VirtualJudgeSpider import config


# Create your views here.

class ContestAPI(APIView):
    def get(self, request, contest_id, *args, **kwargs):
        problems = ContestProblem.objects.filter(contest_id=contest_id)
        serializers = ContestProblemSerializer(problems, many=True)
        res_list = serializers.data
        for item in res_list:
            remote_oj = item['remote_oj']
            remote_id = item['remote_id']
            if Submission.objects.filter(remote_oj=remote_oj, remote_id=remote_id, user=str(request.user),
                                         verdict_code=config.Result.VerdictCode.STATUS_ACCEPTED.value).exists():
                item['status'] = 0
            elif Submission.objects.filter(remote_oj=remote_oj, user=str(request.user), remote_id=remote_id).exists():
                item['status'] = 1
            else:
                item['status'] = 2
        return Response(res_format(res_list))

    def delete(self, request, contest_id, *args, **kwargs):
        Contest.objects.filter(id=contest_id).delete()
        return Response(res_format('delete success'))


class ContestNewAPI(APIView):
    def post(self, request, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False:
            return Response(res_format('Login required', status=Message.ERROR), status=status.HTTP_200_OK)
        if request.user.is_admin is False:
            return Response(res_format('Admin required', status=Message.ERROR), status=status.HTTP_200_OK)

        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():
            contest = serializer.save(request.user)
            if contest:
                return Response(res_format(contest.id), status=status.HTTP_200_OK)
            return Response(res_format('System error', status=Message.ERROR), status=status.HTTP_200_OK)
        return Response(res_format(serializer.errors, status=Message.ERROR), status=status.HTTP_200_OK)


class ContestListAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            contests = Contest.objects.all().order_by('-created_time')[:20]
            serializer = ContestListSerializer(contests, many=True)
            return Response(res_format(serializer.data), status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(res_format('System error', status=Message.ERROR))
