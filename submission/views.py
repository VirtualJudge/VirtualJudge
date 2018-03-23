from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View

from problem.models import Problem
from submission.forms import SubmissionForm
from submission.models import Submission
from submission.serializers import SubmissionSerializer, SubmissionListSerializer
from submission.tasks import submit_task
from utils.decorator import token_required
from utils.request import JudgeRequest
from utils.response import *


class SubmissionShowAPI(View):
    @token_required
    def get(self, request, *args, **kwargs):
        try:
            submission_id = kwargs['submission_id']
            submission = Submission.objects.get(id=submission_id)
            serializer = SubmissionSerializer(submission)
            return JsonResponse(success(serializer.data))
        except Exception as e:
            print(e)
            return JsonResponse(error("get submission error"))


class SubmissionAPI(View):
    @token_required
    def post(self, request):
        form = SubmissionForm(request.POST)
        if form.is_valid():
            problem_id = form.cleaned_data['problem_id']
            code = form.cleaned_data['code']
            language = form.cleaned_data['language']
            try:
                problem = Problem.objects.get(id=problem_id)
                submission = Submission(problem_id=problem_id,
                                        token=request.GET.get('token'),
                                        code=code,
                                        language=language,
                                        remote_id=problem.remote_id,
                                        remote_oj=problem.remote_oj, status=JudgeRequest.status['PENDING'])
                submission.save()
                submit_task.delay(submission.id)
                return JsonResponse(success("submission success"))
            except ObjectDoesNotExist:
                return JsonResponse(error('problem is not exist'))
            except Exception as e:
                return JsonResponse(error('system error'))
        return JsonResponse(error('form is not valid'))


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
            serializers = SubmissionListSerializer(submissions, many=True)
            return JsonResponse(success(serializers.data))
        except Exception as e:
            print(e)
            return JsonResponse(error('error'))


class ReJudgeAPI(View):
    @token_required
    def get(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
            if submission.status != JudgeRequest.status['SUCCESS'] and submission.token == request.GET.get('token'):
                submission.retry_count = 0
                submission.save()
                submit_task.relay(submission_id)
                return JsonResponse(success('rejudge submit success'))
        except:
            pass
        return JsonResponse(error('rejudge failed'))
