from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST, require_GET

from account.forms import PostRegisterForm, PostLoginForm
from account.models import User
from utils import response


class RegisterAPI(View):
    def post(self, request):
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
                return JsonResponse(response.success('register success'))
            except IntegrityError:
                return JsonResponse(response.error('the username has registered'))
        return JsonResponse(response.error('register post data is not valid'))


class LoginAPI(View):
    def post(self, request):
        form = PostLoginForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username'].strip()
                password = form.cleaned_data['password'].strip()
                user = auth.authenticate(username=username, password=password)
                if user:
                    return JsonResponse(response.success('success login'))
                return JsonResponse(response.error('authenticate error'))
            except EnvironmentError:
                return JsonResponse(response.info('exception'))
        return JsonResponse(response.error('login post data is not valid'))


class LogoutAPI(View):
    def post(self, request):
        auth.logout(request)
        return JsonResponse(response.info('logout success'))


@require_GET
@login_required
def get_personal_profile(request):
    # TODO
    pass


@require_POST
@login_required
def update_personal_profile(request):
    # TODO
    pass


def get_public_profile(request):
    # TODO
    pass
