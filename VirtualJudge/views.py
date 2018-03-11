from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from utils import custom_dict


@require_GET
def check_status(request):
    return HttpResponse('Success')


def login_required_url(request):
    return JsonResponse(custom_dict.error('login required'))
