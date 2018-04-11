from django.contrib import auth
from django.db import DatabaseError, IntegrityError
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from account.bodys import LoginBody, RegisterBody
from account.models import UserProfile
from utils.response import *


class LoginAPI(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('login required')

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = LoginBody(request.body)
        if body.is_valid():
            username = body.cleaned_data['username']
            password = body.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponse(success('login success'))
            else:
                return HttpResponse(error('username or password error'))
        return HttpResponse(error(body.errors))


class LogoutAPI(View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponse(success('logout success'))


class RegisterAPI(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = RegisterBody(request.body)
        if body.is_valid():
            username = body.cleaned_data['username']
            password = body.cleaned_data['password']
            email = body.cleaned_data['email']
            try:
                username = UserProfile.objects.create_user(email=email, username=username, password=password)
                username.save()
                return HttpResponse(success('register success'))
            except IntegrityError as e:
                print(e, dir(e))
                print(e.args)
                return HttpResponse(error('User or Email Exist'))
            except DatabaseError:
                return HttpResponse(error('database error'))
        else:
            return HttpResponse(error(body.errors))
