from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from utils import response


@require_GET
def check_status(request):
    return HttpResponse('Success')


