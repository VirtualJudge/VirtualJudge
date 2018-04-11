from django.http import HttpResponse
from django.contrib import auth
from utils.response import error
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from utils.response import *
from account.forms import *
from account.models import UserProfile
from django.db import DatabaseError, IntegrityError
import traceback


def token_not_valid(request, *args, **kwargs):
    return HttpResponse(error('token not valid'))


class LoginAPI(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('login required')

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponse(success('login success'))
            else:
                return HttpResponse(error('username or password error'))
        return HttpResponse(error(form.errors))


class LogoutAPI(View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponse(success('logout success'))


class RegisterAPI(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            try:
                username = UserProfile.objects.create_user(email=email, username=username, password=password)
                username.save()
                return HttpResponse(success('register success'))
            except IntegrityError as e:
                return HttpResponse(error('User or Email Exist'))
            except DatabaseError:
                return HttpResponse(error('database error'))
        else:
            return HttpResponse(error(form.errors))
