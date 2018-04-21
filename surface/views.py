from django.shortcuts import render
from django.views import View


# Create your views here.

class ProfileAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html')


class IndexAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class ProblemsAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'problems.html')


class ProblemAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'problem.html')


class HelpAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'help.html')


class RankAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rank.html')


class SubmisssionsAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'submissions.html')


class SubmisssionAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'submission.html')


class ContestsAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contests.html')


class ContestAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contest/index.html')


class ContestNewAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contest/new.html')


class RegisterAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')


class LoginAPI(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')
