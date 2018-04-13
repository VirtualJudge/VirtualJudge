from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from .serializers import ContestSerializer
from utils.response import res_format, Message


# Create your views here.

class ContestAPI(APIView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False:
            return Response(res_format('login required', status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)
        serializer = ContestSerializer(data=request.data)
        if serializer.is_valid():
            contest = serializer.save(request.user)
            if contest:
                return Response(res_format(contest.id), status=status.HTTP_200_OK)
            return Response(res_format('system error'), status=status.HTTP_400_BAD_REQUEST)
        return Response(res_format(serializer.errors, status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)
