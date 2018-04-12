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


class LanguagesAPI(APIView):

    def get(self, request, *args, **kwargs):
        oj_name = kwargs['remote_oj']
        if Control.Controller.is_support(kwargs['remote_oj']):
            remote_oj = Control.Controller.get_real_remote_oj(oj_name)
            languages = Language.objects.filter(oj_name=remote_oj)
            return Response(res_format(LanguagesSerializer(languages).data), status=status.HTTP_200_OK)
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
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            remote_oj = serializer.validated_data['remote_oj']
            try:
                acc = Account.objects.get(oj_name=remote_oj, oj_username=username)
                acc.oj_password = password
                acc.save()
                return Response(res_format('success update account password ' + str(username)),
                                status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                Account(oj_name=remote_oj, oj_username=username, oj_password=password).save()
                return Response(res_format('success create account ' + str(username)), status=status.HTTP_200_OK)
            except DatabaseError:
                return Response(res_format('error update account ' + str(username), status=Message.ERROR),
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(res_format(serializer.errors, status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)
