import json
import traceback

from django.http import JsonResponse
from django.views import View

from config.forms import RemoteAccountForm
from config.models import RemoteAccount, RemoteOJ
from config.tasks import update_remote_language_task
from utils import response
from VirtualJudgeSpider.Control import Controller


class InitRemoteAPI(View):
    def post(self, request, **kwargs):
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
                return JsonResponse(response.success('success update account'))
            except:
                traceback.print_exc()
        return JsonResponse(response.error("error update account"))
