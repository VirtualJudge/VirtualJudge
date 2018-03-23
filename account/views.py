from django.http import JsonResponse
from utils.response import error


def token_not_valid(request, *args, **kwargs):
    return JsonResponse(error('token not valid'))
