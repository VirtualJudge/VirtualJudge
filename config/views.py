import json
import traceback

from VirtualJudgeSpider import Control
from VirtualJudgeSpider.Control import Controller
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from config.forms import RemoteAccountForm
from config.models import RemoteAccount, RemoteOJ, RemoteLanguage
from config.serializers import RemoteLanguageSerializer
from config.tasks import update_remote_language_task
from utils import response
from utils.decorator import super_token_required
from utils.response import *


class RemoteLanguageAPI(View):

    def get(self, request, *args, **kwargs):
        oj_name = kwargs['remote_oj']
        if Control.Controller.is_support(kwargs['remote_oj']):
            remote_oj = Controller.get_real_remote_oj(oj_name)
            remote_languages = RemoteLanguage.objects.filter(oj_name=remote_oj)
            return HttpResponse(success(RemoteLanguageSerializer(remote_languages, many=True).data))
        return HttpResponse(error("find language error"))


class InitRemoteAPI(View):
    @super_token_required
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = RemoteAccountForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                RemoteOJ.objects.all().delete()
                remote_oj_list = []
                for remote_oj in Controller.get_supports():
                    remote_oj_list.append(RemoteOJ(oj_name=remote_oj))
                RemoteOJ.objects.bulk_create(remote_oj_list)
                json_str = ""
                for chunk in form.cleaned_data['remote_accounts'].chunks():
                    json_str += chunk.decode('utf-8')
                values = json.loads(json_str)
                remote_s = []
                RemoteAccount.objects.all().delete()
                for value in values:
                    if value['remote_oj'] and value['username'] and value['password']:
                        remote_s.append(RemoteAccount(oj_name=value['remote_oj'], oj_username=value['username'],
                                                      oj_password=value['password']))
                RemoteAccount.objects.bulk_create(remote_s)
                update_remote_language_task.delay()
                return HttpResponse(response.success('success update account'))
            except:
                traceback.print_exc()
        return HttpResponse(response.error("error update account"))
