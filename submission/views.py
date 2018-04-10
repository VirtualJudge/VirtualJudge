from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from problem.models import Problem
from submission.forms import SubmissionForm
from submission.models import Submission
from submission.serializers import SubmissionSerializer, SubmissionListSerializer
from submission.tasks import submit_task
from utils.decorator import token_required, super_token_required
from utils.request import JudgeRequest
from utils.response import *
from VirtualJudgeSpider import Config


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
    @csrf_exempt
    def post(self, request):
        form = SubmissionForm(request.POST)
        if form.is_valid():
            remote_oj = form.cleaned_data['remote_oj']
            remote_id = form.cleaned_data['remote_id']
            code = form.cleaned_data['code']
            language = form.cleaned_data['language']
            try:
                problem = Problem.objects.get(remote_oj=remote_oj, remote_id=remote_id)
                submission = Submission(problem_id=problem.id,
                                        token=request.GET.get('token'),
                                        code=code,
                                        language=language,
                                        remote_id=problem.remote_id,
                                        remote_oj=problem.remote_oj)
                submission.save()
                submit_task.delay(submission.id)
                return JsonResponse(success("submission success:" + str(submission.id)))
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
    @super_token_required
    def get(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
            if submission.status != Config.Result.Status.STATUS_RESULT_GET.value:
                submission.save()
                submit_task.relay(submission_id)
                return JsonResponse(success('rejudge submit success'))
        except:
            pass
        return JsonResponse(error('rejudge failed'))
