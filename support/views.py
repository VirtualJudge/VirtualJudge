from django.db import DatabaseError
from rest_framework import status
from rest_framework.views import APIView, Response
from spider.core import Core
from django.db.models import F, Q
from support.models import Language, Account, Support
from support.serializers import AccountSerializer
from support.serializers import LanguagesSerializer
from support.serializers import SupportSerializer
from support.serializers import UpdateEnableSerializer
from support.serializers import UpdateProxiesSerializer
from support.tasks import update_language_task
from utils.response import res_format, Message
from support.tasks import update_oj_status


class SupportAdminAPI(APIView):
    def get(self, request, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False or request.user.is_admin is False:
            return Response(res_format('Permission Denied', status=Message.ERROR), status=status.HTTP_200_OK)
        support = Support.objects.all()
        return Response(res_format(SupportSerializer(support, many=True).data))

    def post(self, request, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False or request.user.is_admin is False:
            return Response(res_format('Permission Denied', status=Message.ERROR), status=status.HTTP_200_OK)
        request_type = request.GET.get('type')
        if request_type == 'enable':
            serializer = UpdateEnableSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(res_format('success'))
            else:
                print(serializer.errors)
                return Response(res_format('error', Message.ERROR))
        elif request_type == 'fresh':
            platform = request.GET.get('platform')
            if platform:
                update_oj_status.delay(platform)
            else:
                try:
                    for item in Core.get_supports():
                        if not Support.objects.filter(oj_name=item):
                            Support.objects.create(oj_name=item).save()
                        Support.objects.filter(oj_name=item).update(oj_status='PENDING')
                        update_oj_status.delay(item)
                except Exception as e:
                    print(e)
                    return Response(res_format('error', Message.ERROR))
                return Response(res_format('success'))
        elif request_type == 'proxies':
            serializer = UpdateProxiesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(res_format('success'))
            else:
                return Response(res_format('error', Message.ERROR))
        support = list({item.oj_name for item in Support.objects.filter(oj_enable=True)})
        support.sort()
        return Response(res_format(support), status=status.HTTP_200_OK)


class SupportAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            support = list({item.oj_name for item in Support.objects.filter(oj_enable=True)})
            support.sort()
            return Response(res_format(support), status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(res_format('System error', status=Message.ERROR),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccountAPI(APIView):
    def get(self, request, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False or request.user.is_admin is False:
            return Response(res_format('Permission Denied', status=Message.ERROR), status=status.HTTP_200_OK)
        accounts = Account.objects.all().order_by('-id')
        return Response(res_format(AccountSerializer(accounts, many=True).data))

    def post(self, request, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False or request.user.is_admin is False:
            return Response(res_format('Permission Denied', status=Message.ERROR), status=status.HTTP_200_OK)
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.save():
                update_language_task.delay(serializer.validated_data['oj_name'])
                return Response(res_format('success'), status=status.HTTP_200_OK)
            else:
                return Response(res_format('error', status=Message.ERROR),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(res_format(serializer.errors, status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False or request.user.is_admin is False:
            return Response(res_format('Permission Denied', status=Message.ERROR), status=status.HTTP_200_OK)
        platform = request.GET.get('platform')
        username = request.GET.get('username')
        if platform and username:
            try:
                Account.objects.filter(oj_name=platform, oj_username=username).delete()
                return Response(res_format('success'))
            except:
                pass
        return Response(res_format('error', Message.ERROR))


class LanguageAPI(APIView):

    def get(self, request, *args, **kwargs):
        remote_oj = request.GET.get('platform')
        if remote_oj is None:
            return Response(res_format('platform required', status=Message.ERROR),
                            status=status.HTTP_400_BAD_REQUEST)
        if Core.is_support(remote_oj):
            try:
                languages = Language.objects.filter(oj_name=remote_oj)
                return Response(res_format(LanguagesSerializer(languages, many=True).data), status=status.HTTP_200_OK)
            except DatabaseError:
                return Response(res_format('System error', status=Message.ERROR),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res_format('we do not support it', status=Message.ERROR), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False or request.user.is_admin is False:
            return Response(res_format('Admin required', status=Message.ERROR), status=status.HTTP_200_OK)
        try:
            accounts = Account.objects.all()
            for remote_oj in {account.oj_name for account in accounts}:
                update_language_task.delay(remote_oj)
            return Response(res_format('Freshed successfully'), status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(res_format('Freshed error', status=Message.ERROR),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
