from datetime import datetime

from VirtualJudgeSpider import Config
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from contest.models import Contest
from problem.models import Problem
from remote.models import Language
from submission.bodys import SubmissionBody
from submission.models import Submission
from submission.serializers import SubmissionSerializer, SubmissionListSerializer, VerdictSerializer
from submission.tasks import submit_task
from utils.response import *


class VerdictAPI(View):
    def get(self, request, *args, **kwargs):
        try:
            submission_id = kwargs['submission_id']
            submission = Submission.objects.get(id=submission_id)
            return HttpResponse(success(VerdictSerializer(submission).data))
        except:
            return HttpResponse(error("some error occurred"))


class SubmissionShowAPI(View):
    def get(self, request, *args, **kwargs):
        try:
            submission_id = kwargs['submission_id']
            submission = Submission.objects.get(id=submission_id)
            serializer = SubmissionSerializer(submission)
            return HttpResponse(success(serializer.data))
        except Exception as e:
            return HttpResponse(error("get submission error"))


class SubmissionAPI(View):
    @method_decorator(login_required)
    @csrf_exempt
    def post(self, request):
        last_submit_time = request.session.get('last_submit_time', None)
        if last_submit_time and (datetime.now() - datetime.fromtimestamp(last_submit_time)).seconds < 5:
            return HttpResponse(error("五秒内不能再次提交"))
        request.session['last_submit_time'] = datetime.now().timestamp()
        body = SubmissionBody(request.body)
        if body.is_valid():
            remote_oj = body.cleaned_data('remote_oj')
            remote_id = body.cleaned_data('remote_id')
            contest_id = body.cleaned_data('contest_id')
            source_code = body.cleaned_data('source_code')
            language = body.cleaned_data('language')
            try:
                problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
                language = Language.objects.get(remote_oj=remote_oj, oj_language=language)
                if contest_id is not None:
                    submission = Submission(problem_id=problem.id,
                                            user=request.user,
                                            code=source_code,
                                            contest_id=contest_id,  # 找不同
                                            language=language,
                                            remote_id=problem.remote_id,
                                            remote_oj=problem.remote_oj)
                else:
                    submission = Submission(problem_id=problem.id,
                                            user=request.user,
                                            code=source_code,
                                            language=language,
                                            remote_id=problem.remote_id,
                                            remote_oj=problem.remote_oj)
                submission.save()
                submit_task.delay(submission.id)
                return HttpResponse(success({'submission_id': submission.id}))
            except:
                return HttpResponse(error('submission error'))
        else:
            return HttpResponse(error(body.errors))


class SubmissionListAPI(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        try:
            offset = 0
            limit = 20
            for k, v in kwargs.items():
                if k == 'offset':
                    offset = v
                if k == 'limit':
                    limit = v
            submissions = Submission.objects.filter(contest_id=None).order_by('-id')[offset:offset + limit]
            return HttpResponse(success(SubmissionListSerializer(submissions, many=True).data))
        except Exception as e:
            print(e)
            return HttpResponse(error('error'))


class ReJudgeAPI(View):
    @method_decorator(login_required)
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
