from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View

from submission.tasks import submit_task
from problem.models import Problem
from submission.forms import SubmissionForm
from submission.models import Submission
from submission.serializers import SubmissionSerializer, SubmissionListSerializer
from utils import response
from utils.request import JudgeRequest


class SubmissionShowAPI(View):
    def get(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
            serializer = SubmissionSerializer(submission)
            return JsonResponse(serializer.data)
        except Exception as e:
            print(e)
            return JsonResponse(response.error("get submission error"))


class SubmissionAPI(View):
    def post(self, request):
        form = SubmissionForm(request.POST)
        if form.is_valid():
            problem_id = form.cleaned_data['problem_id']
            code = form.cleaned_data['code']
            language = form.cleaned_data['language']
            try:
                problem = Problem.objects.get(id=problem_id)
                submission = Submission(problem_id=problem_id,
                                        code=code,
                                        language=language,
                                        remote_id=problem.remote_id,
                                        remote_oj=problem.remote_oj, status=JudgeRequest.status['PENDING'])
                submission.save()
                submit_task.delay(submission.id)
                return JsonResponse(response.success("submission success"))
            except ObjectDoesNotExist:
                return JsonResponse(response.error('problem is not exist'))
            except Exception as e:
                print(e)
                return JsonResponse(response.error('system error'))
        return JsonResponse(response.error('form is not valid'))


class SubmissionListAPI(View):
    def get(self, request, offset=0, limit=10):
        try:
            submissions = Submission.objects.all().order_by('-id')[offset:offset + limit]
            serializers = SubmissionListSerializer(submissions, many=True)
            return JsonResponse(serializers.data)
        except:
            return JsonResponse(response.error('error'))


class ReJudgeAPI(View):
    def get(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
            if submission.status != JudgeRequest.status['SUCCESS']:
                submission.retry_count = 0
                submission.save()
                submit_task.relay(submission_id)
                return JsonResponse(response.success('rejudge submit'))
        except:
            pass
        return JsonResponse(response.error('rejudge failed'))
