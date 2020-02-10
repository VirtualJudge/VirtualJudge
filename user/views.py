from django.contrib import auth
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.viewsets import GenericViewSet

from user.models import Profile
from user.serializers import (LoginSerializer, RegisterSerializer, PasswordSerializer, UserProfileSerializer)
from util.message import Message


class UserAPI(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Profile.objects.all()
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'
    serializer_class = UserProfileSerializer
    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserProfileSerializer(user)
    #     return Response(Message.success(data=serializer.data))
    #
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = UserProfileSerializer(queryset, many=True)
    #     return Response(Message.success(data=serializer.data))


class PasswordAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            result, message = serializer.save()
            if result:
                auth.logout(request)
                return Response(Message.success(msg=message))
            else:
                return Response(Message.error(msg=message))
        else:
            return Response(Message.error(msg=serializer.errors))


class ProfileAPI(APIView):
    # 获取个人信息
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            profile = Profile.objects.get(username=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(Message.success(data=serializer.data))
        return Response(Message.error(msg='Unauthorized'))

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(Message.success(data=serializer.data))
        else:
            return Response(Message.error(msg=serializer.errors))


class AuthAPI(APIView):
    # 检查登录状态
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return Response(Message.success(data=UserProfileSerializer(request.user).data))
        return Response(Message.error(msg='Unauthorized'))

    # 提交登录
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.login(request)
            if user:
                return Response(Message.success(data=UserProfileSerializer(user).data))
            else:
                return Response(Message.error(msg='Incorrect username or password'))
        return Response(Message.error(msg=serializer.errors))

    # 退出登录
    def delete(self, request, **kwargs):
        auth.logout(request)
        return Response(Message.success(msg='Logout success'))


class RegisterAPI(APIView):
    def post(self, request, *args, **kwargs):
        register = RegisterSerializer(data=request.data)
        if register.is_valid():
            result, message = register.save()
            if result:
                return Response(Message.success(msg=message))
            else:
                return Response(Message.error(msg=message))
        return Response(Message.error(msg=register.errors))
