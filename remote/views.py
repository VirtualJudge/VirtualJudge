import traceback

from VirtualJudgeSpider import Control
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from remote.bodys import AccountBody
from remote.models import Account, OJ, Language
from remote.serializers import RemoteLanguageSerializer
from remote.tasks import update_remote_language_task
from utils import response
from utils.response import *


class RemoteLanguageAPI(View):

    def get(self, request, *args, **kwargs):
        oj_name = kwargs['remote_oj']
        if Control.Controller.is_support(kwargs['remote_oj']):
            remote_oj = Control.Controller.get_real_remote_oj(oj_name)
            remote_languages = Language.objects.filter(oj_name=remote_oj)
            return HttpResponse(success(RemoteLanguageSerializer(remote_languages, many=True).data))
        return HttpResponse(error("find language error"))


class RemoteAPI(View):
    @method_decorator(login_required)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.user.is_admin is False:
            return HttpResponse(response.error("admin required"))
        body = AccountBody(request.body)
        if body.is_valid():
            account = body.cleaned_data('account')
            try:
                OJ.objects.all().delete()
                OJ.objects.bulk_create([OJ(oj_name) for oj_name in Control.Controller.get_supports()])
                values = json.loads(account)
                Account.objects.all().delete()
                Account.objects.bulk_create([Account(oj_name=value['remote_oj'], oj_username=value['username'],
                                                     oj_password=value['password']) for value in values])

                update_remote_language_task.delay()
                return HttpResponse(response.success('success update account'))
            except:
                traceback.print_exc()
                return HttpResponse(response.error("error update account"))
        else:
            return HttpResponse(response.error(body.errors))
