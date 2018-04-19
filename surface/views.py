from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page


# Create your views here.

class IndexAPI(View):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class ProblemsAPI(View):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return render(request, 'problems.html')


class ProblemAPI(View):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return render(request, 'problem.html')


class SubmisssionsAPI(View):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return render(request, 'submissions.html')


class SubmisssionAPI(View):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return render(request, 'submission.html')


class ContestsAPI(View):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return render(request, 'contests.html')


class ContestNewAPI(View):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return render(request, 'contest/new.html')


class RegisterAPI(View):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')


class LoginAPI(View):
    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
