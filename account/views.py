from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from account.serializers import (LoginSerializer, RegisterSerializer,
                                 UserProfileSerializer)
from utils.response import res_format, Message
from django.contrib import auth


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        return Response(res_format('login required', Message.ERROR),
                        status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def get(self, request, **kwargs):
        return Response(res_format('login required', Message.ERROR),
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.login(request)
            if user:
                return Response(res_format(UserProfileSerializer(user).data,
                                           Message.SUCCESS),
                                status=status.HTTP_200_OK)
            else:
                return Response(res_format('username or password not correct',
                                           Message.ERROR),
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(res_format(serializer.errors, Message.ERROR),
                        status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    def delete(self, request, **kwargs):
        auth.logout(request)
        return Response(res_format('logout success'),
                        status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    @csrf_exempt
    def post(self, request, **kwargs):
        register = RegisterSerializer(data=request.data)
        if register.is_valid():
            if register.save():
                return Response(res_format('register success'),
                                status=status.HTTP_200_OK)
            else:
                return Response(res_format('system error'),
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(res_format(register.errors),
                        status=status.HTTP_400_BAD_REQUEST)
