from django.shortcuts import render
from django.views.decorators.cache import cache_page


# Create your views here.
@cache_page(60 * 15)
def index(request):
    return render(request, 'index.html')


@cache_page(60 * 15)
def problems(request):
    return render(request, 'problems.html')


@cache_page(60 * 15)
def problem(request):
    return render(request, 'problem.html')


@cache_page(60 * 15)
def submissions(request):
    return render(request, 'submissions.html')


@cache_page(60 * 15)
def contests(request):
    return render(request, 'contests.html')


@cache_page(60 * 15)
def contest_new(request):
    return render(request, 'contest/new.html')


@cache_page(60 * 15)
def register(request):
    return render(request, 'register.html')


@cache_page(60 * 15)
def login(request):
    return render(request, 'login.html')
