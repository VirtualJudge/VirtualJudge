from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def check_status(request):
    return HttpResponse('Virtual Judge Status Success\n')
