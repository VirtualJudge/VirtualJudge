from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html')


def problem(request):
    return render(request, 'problem.html')


def status(request):
    return render(request, 'status.html')


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')
