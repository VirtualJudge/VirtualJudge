from django.contrib import auth
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from user.models import Profile
from user.serializers import (LoginSerializer, RegisterSerializer, PasswordSerializer, UserProfileSerializer)


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
                return Response(message)
            else:
                return Response(message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPI(APIView):
    # 获取个人信息
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            profile = Profile.objects.get(username=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPI(APIView):
    # 检查登录状态
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return Response(UserProfileSerializer(request.user).data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # 提交登录
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.login(request)
            if user:
                return Response(UserProfileSerializer(user).data)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 退出登录
    def delete(self, request, **kwargs):
        auth.logout(request)
        return Response(data='OK')


class RegisterAPI(APIView):
    def post(self, request, *args, **kwargs):
        register = RegisterSerializer(data=request.data)
        if register.is_valid():
            result, message = register.save()
            if result:
                return Response(message)
            else:
                return Response(message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(register.errors, status=status.HTTP_400_BAD_REQUEST)
