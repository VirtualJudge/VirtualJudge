from functools import wraps
from account.views import token_not_valid
from account.models import Token
import traceback


def super_token_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            if not token or Token.objects.get(token=token).privilege < 2:
                return token_not_valid(request, *args, **kwargs)
        except:
            traceback.print_exc()
            return token_not_valid(request, *args, **kwargs)
        return func(self, request, *args, **kwargs)
    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            if not (token and Token.objects.get(token=token)):
                return token_not_valid(request, *args, **kwargs)
        except:
            traceback.print_exc()
        return func(self, request, *args, **kwargs)

    return wrapper
