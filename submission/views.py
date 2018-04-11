import traceback

from VirtualJudgeSpider import Config
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from problem.models import Problem
from submission.models import Submission
from submission.serializers import SubmissionSerializer, SubmissionListSerializer, VerdictSerializer
from submission.tasks import submit_task
from utils.decorator import token_required
from utils.response import *
from datetime import datetime


class VerdictAPI(View):

    def get(self, request, *args, **kwargs):
        try:
            submission_id = kwargs['submission_id']
            submission = Submission.objects.get(id=submission_id)
            return HttpResponse(success(VerdictSerializer(submission).data))
        except:
            return HttpResponse(error("some error occurred"))


class SubmissionShowAPI(View):
    @token_required
    def get(self, request, *args, **kwargs):
        try:
            submission_id = kwargs['submission_id']
            submission = Submission.objects.get(id=submission_id)
            serializer = SubmissionSerializer(submission)
            return HttpResponse(success(serializer.data))
        except Exception as e:
            return HttpResponse(error("get submission error"))


class SubmissionAPI(View):
    @token_required
    @csrf_exempt
    def post(self, request):
        last_submit_time = request.session.get('last_submit_time', None)
        if last_submit_time and (datetime.now() - datetime.fromtimestamp(last_submit_time)).seconds < 5:
            return HttpResponse(error("五秒内不能再次提交"))
        request.session['last_submit_time'] = datetime.now().timestamp()
        remote_oj = request.POST['remote_oj']
        remote_id = request.POST['remote_id']
        code_file = request.FILES['source_code']
        language = request.POST['language']
        try:
            source_code = ''
            for chunk in code_file.chunks():
                source_code += chunk.decode('utf-8')
            problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
            submission = Submission(problem_id=problem.id,
                                    token=request.GET.get('token'),
                                    code=source_code,
                                    language=language,
                                    remote_id=problem.remote_id,
                                    remote_oj=problem.remote_oj)
            submission.save()
            submit_task.delay(submission.id)
            return HttpResponse(success({'submission_id': submission.id}))
        except ObjectDoesNotExist:
            return HttpResponse(error('problem is not exist'))
        except Exception as e:
            traceback.print_exc()
            return HttpResponse(error('system error'))


class SubmissionListAPI(View):
    @token_required
    def get(self, request, *args, **kwargs):
        try:
            offset = 0
            limit = 20
            for k, v in kwargs.items():
                if k == 'offset':
                    offset = v
                if k == 'limit':
                    limit = v
            submissions = Submission.objects.filter(token=request.GET.get('token')).order_by('-id')[
                          offset:offset + limit]
            return HttpResponse(success(SubmissionListSerializer(submissions, many=True).data))
        except Exception as e:
            print(e)
            return HttpResponse(error('error'))


class ReJudgeAPI(View):
    @token_required
    def get(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
            if submission.status in {Config.Result.Status.STATUS_NO_ACCOUNT.value,
                                     Config.Result.Status.STATUS_NETWORK_ERROR.value}:
                submission.status = Config.Result.Status.STATUS_PENDING.value
                submission.save()
                submit_task.delay(submission_id)
                return HttpResponse(success('rejudge submit success'))
        except:
            pass
        return HttpResponse(error('rejudge failed'))
