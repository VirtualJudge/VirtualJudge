from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response

from account.serializers import *
from utils.response import *


class LoginAPI(APIView):
    def get(self, request, format=None):
        return Response(res_format('login required', Message.ERROR), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = auth.authenticate(username=serializer.validated_data['username'],
                                     password=serializer.validated_data['password'])
            if user is not None:
                auth.login(request, user)
                return Response(res_format(UserProfileSerializer(user).data, Message.SUCCESS),
                                status=status.HTTP_200_OK)
            else:
                return Response(res_format('password not correct', Message.ERROR), status=status.HTTP_400_BAD_REQUEST)
        return Response(res_format(serializer.errors, Message.ERROR), status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):

    def delete(self, request, format=None):
        auth.logout(request)
        return Response(res_format('logout success'), status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        print(dir(request))
        print(request.data)
        register = RegisterSerializer(data=request.data)
        if register.is_valid():
            register.save()
            return Response(res_format('register success'), status=status.HTTP_200_OK)
        return Response(res_format(register.errors), status=status.HTTP_400_BAD_REQUEST)
