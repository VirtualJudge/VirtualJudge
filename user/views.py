import hashlib
from django.http import Http404
from django.contrib import auth
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from user.models import Profile
from user.serializers import (LoginSerializer, RegisterSerializer, PasswordSerializer, UserProfileSerializer)
from util.message import Message


class UserViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Profile.objects.all()
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]{32}'

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)


class PasswordViewSet(GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = PasswordSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]{32}'

    def get_object(self, pk=None, *args, **kwargs):
        try:
            return Profile.objects.get(id=pk)
        except Profile.DoesNotExist:
            raise Http404

    def update(self, request, pk=None, *args, **kwargs):
        if request.user.is_admin:
            user = self.get_object(pk=pk)
        else:
            user = self.get_object(pk=request.user.id)
        serializer = PasswordSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPI(APIView):
    # 获取个人信息
    def get(self, request, **kwargs):
        if request.user and request.user.is_authenticated:
            user_profile = Profile.objects.get(username=request.user)
            serializer = UserProfileSerializer(user_profile)
            res_data = serializer.data
            res_data['email'] = hashlib.md5(str(res_data['email']).encode('utf-8')).hexdigest()
            return Response(Message.success(data=res_data))
        return Response(Message.error(msg='not login'))


class AuthAPI(APIView):
    # 检查登录状态
    def get(self, request, **kwargs):
        if request.user and request.user.is_authenticated:
            return Response(Message.success(data=str(request.user)))
        return Response(Message.error(msg='Login required'))

    # 提交登录
    def post(self, request, **kwargs):
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
    def post(self, request, **kwargs):
        register = RegisterSerializer(data=request.data)
        if register.is_valid():
            if register.save():
                return Response(Message.success(msg='Register succeed'))
            else:
                return Response(Message.error(msg='System error'))
        return Response(Message.error(msg=register.errors))
