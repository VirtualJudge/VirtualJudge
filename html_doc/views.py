from django.views import View
from django.shortcuts import render


class HomeAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class LoginAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


class RegisterAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')
