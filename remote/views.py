import traceback

from VirtualJudgeSpider import Control
from VirtualJudgeSpider.Control import Controller
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from remote.forms import RemoteAccountForm
from remote.models import Account, OJ, Language
from remote.serializers import RemoteLanguageSerializer
from remote.tasks import update_remote_language_task
from utils import response
from utils.response import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class RemoteLanguageAPI(View):

    def get(self, request, *args, **kwargs):
        oj_name = kwargs['remote_oj']
        if Control.Controller.is_support(kwargs['remote_oj']):
            remote_oj = Controller.get_real_remote_oj(oj_name)
            remote_languages = Language.objects.filter(oj_name=remote_oj)
            return HttpResponse(success(RemoteLanguageSerializer(remote_languages, many=True).data))
        return HttpResponse(error("find language error"))


class RemoteAPI(View):
    @method_decorator(login_required)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.user.is_admin is False:
            return HttpResponse(response.error("admin required"))
        form = RemoteAccountForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                OJ.objects.all().delete()
                remote_oj_list = []
                for remote_oj in Controller.get_supports():
                    remote_oj_list.append(OJ(oj_name=remote_oj))
                OJ.objects.bulk_create(remote_oj_list)
                json_str = ""
                for chunk in form.cleaned_data['remote_accounts'].chunks():
                    json_str += chunk.decode('utf-8')
                values = json.loads(json_str)
                remote_s = []
                Account.objects.all().delete()
                for value in values:
                    if value['remote_oj'] and value['username'] and value['password']:
                        remote_s.append(Account(oj_name=value['remote_oj'], oj_username=value['username'],
                                                oj_password=value['password']))
                Account.objects.bulk_create(remote_s)
                update_remote_language_task.delay()
                return HttpResponse(response.success('success update account'))
            except:
                traceback.print_exc()
        return HttpResponse(response.error("error update account"))
