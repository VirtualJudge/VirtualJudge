from django.contrib import auth
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.views import Response

from account.serializers import (LoginSerializer, RegisterSerializer, ChangePasswordSerializer,
                                 UserProfileSerializer)
from utils.response import res_format, Message


class ChangePasswordAPI(APIView):
    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.change_password()
                if user is not None:
                    return Response(res_format(UserProfileSerializer(user).data, status=Message.SUCCESS))
                return Response(res_format('Change password failed', status=Message.ERROR))
            return Response(res_format(serializer.errors, status=Message.ERROR))
        return Response(res_format('Login required', status=Message.ERROR))


class SessionAPI(APIView):
    def post(self, request, **kwargs):
        if request.user and request.user.is_authenticated:
            return Response(res_format(str(request.user), status=Message.SUCCESS))
        return Response(res_format('Login required', status=Message.ERROR))


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        return Response(res_format('Login required', Message.ERROR))


class LoginAPI(APIView):
    def get(self, request, **kwargs):
        return Response(res_format('Login required', Message.ERROR))

    def post(self, request, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.login(request)
            if user:
                return Response(res_format(UserProfileSerializer(user).data, Message.SUCCESS),
                                status=status.HTTP_200_OK)
            else:
                return Response(res_format('Incorrect username or password', Message.ERROR))
        return Response(res_format(serializer.errors, Message.ERROR))


class LogoutAPI(APIView):
    def delete(self, request, **kwargs):
        auth.logout(request)
        return Response(res_format('Logout success'))


class RegisterAPI(APIView):
    def post(self, request, **kwargs):
        register = RegisterSerializer(data=request.data)
        if register.is_valid():
            if register.save():
                return Response(res_format('Register success'))
            else:
                return Response(res_format('System error', status=Message.ERROR))
        return Response(res_format(register.errors, status=Message.ERROR))
