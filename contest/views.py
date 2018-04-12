from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

class ContestAPI(View):
    def get(self, request, *args, **kwargs):
        pass

    @csrf_exempt
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pass
