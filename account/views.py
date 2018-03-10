from django.views.decorators.http import require_POST, require_GET
from account.forms import PostRegisterForm, PostLoginForm
from account.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.db.utils import IntegrityError
from utils import custom_dict
from django.contrib import auth
from django.contrib.auth.decorators import login_required


@require_POST
def register_user(request):
    form = PostRegisterForm(request.POST)
    if form.is_valid():
        try:
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()
            email = form.cleaned_data['email'].strip()

            user = User()
            user.username = username
            user.set_password(password)
            user.email = email
            user.save()
            return JsonResponse(custom_dict.success('ok'))
        except IntegrityError:
            return JsonResponse(custom_dict.error('the username has registered'))
    return JsonResponse(custom_dict.error('register post data is not valid'))


@require_POST
def login_user(request):
    form = PostLoginForm(request.POST)
    if form.is_valid():
        try:
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password'].strip()
            user = auth.authenticate(username=username, password=password)
            if user:
                return JsonResponse(custom_dict.success('yes'))
            return JsonResponse(custom_dict.error('no'))
        except EnvironmentError:
            return JsonResponse(custom_dict.info('exception'))
    return JsonResponse(custom_dict.error('login post data is not valid'))


@require_POST
def logout_user(request):
    auth.logout(request)
    return JsonResponse(custom_dict.info('logout success'))


@require_GET
@login_required
def get_personal_profile(request):
    pass


@require_POST
@login_required
def update_personal_profile(request):
    pass


def get_public_profile(request):
    pass
