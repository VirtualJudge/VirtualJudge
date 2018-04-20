from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response

from utils.response import res_format, Message
from .models import Contest
from .serializers import ContestSerializer, ContestListSerializer
from django.db import DatabaseError


# Create your views here.

class ContestAPI(APIView):
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
    def post(self, request, *args, **kwargs):
        try:
            contests = Contest.objects.all().order_by('-created_time')[:20]
            serializer = ContestListSerializer(contests, many=True)
            return Response(res_format(serializer.data), status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(res_format('System error', status=Message.ERROR))


class ContestProblemList(APIView):
    def post(self, request, contest_id, *args, **kwargs):
        pass


class ContestSubmissionList(APIView):
    def post(self, request, contest_id, *args, **kwargs):
        pass
