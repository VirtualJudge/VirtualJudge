from VirtualJudgeSpider import Control
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView, Response

from remote.models import Account, Language
from remote.serializers import AccountSerializer
from remote.serializers import LanguagesSerializer
from remote.tasks import update_language_task
from utils.response import res_format, Message
from django.db import DatabaseError


class LanguagesAPI(APIView):

    def get(self, request, raw_oj_name, *args, **kwargs):
        remote_oj = Control.Controller.get_real_remote_oj(raw_oj_name)
        if Control.Controller.is_support(remote_oj):
            try:
                languages = Language.objects.filter(oj_name=remote_oj)
                return Response(res_format(LanguagesSerializer(languages, many=True).data), status=status.HTTP_200_OK)
            except DatabaseError:
                return Response(res_format('request error', status=Message.ERROR),
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(res_format('we do not support it', status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)


class FreshLanguageAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        update_language_task.delay()
        return Response(res_format('request update remote language'), status=status.HTTP_200_OK)


class RemoteAPI(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.save():
                return Response(res_format('operation success', status=Message.SUCCESS), status=status.HTTP_200_OK)
            else:
                return Response(res_format('operation failed', status=Message.ERROR),
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(res_format(serializer.errors, status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)
