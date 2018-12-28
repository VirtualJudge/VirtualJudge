from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework import status
from rest_framework.views import APIView, Response
from spider import config

from submission.models import Submission
from submission.serializers import SubmissionListSerializer, VerdictSerializer, SubmissionSerializer
from submission.tasks import submit_task
from utils.response import res_format, Message


class VerdictAPI(APIView):
    def get(self, request, submission_id, *args, **kwargs):
        try:
            submission = Submission.objects.get(id=submission_id)
            if submission.user == str(request.user):
                return Response(res_format(VerdictSerializer(submission).data), status=status.HTTP_200_OK)
            else:
                res_data = VerdictSerializer(submission).data
                res_data['code'] = None
                return Response(res_format(res_data), status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(res_format('submission not exist', status=Message.ERROR), status=status.HTTP_200_OK)


class SubmissionAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get('user'):
                submissions = Submission.objects.filter(user=request.GET.get('user')).order_by('-create_time')[:500]
                return Response(res_format(SubmissionListSerializer(submissions, many=True).data),
                                status=status.HTTP_200_OK)
            submissions = Submission.objects.all().order_by('-create_time')[:500]
            return Response(res_format(SubmissionListSerializer(submissions, many=True).data),
                            status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(res_format('System error', status=Message.ERROR),
                            status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False:
            return Response(res_format('Login required', status=Message.ERROR), status=status.HTTP_200_OK)
        last_submit_time = request.session.get('last_submit_time', None)
        if last_submit_time and (datetime.now() - datetime.fromtimestamp(last_submit_time)).seconds < 5:
            return Response(res_format("Cannot be resubmitted within five seconds", status=Message.ERROR),
                            status=status.HTTP_200_OK)
        request.session['last_submit_time'] = datetime.now().timestamp()

        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save(str(request.user))
            if submission is not None:
                if submission.status != config.Result.Status.STATUS_PENDING.value:
                    return Response(res_format(submission.id), status=status.HTTP_200_OK)
                submit_task.delay(submission.id)
                return Response(res_format(submission.id), status=status.HTTP_200_OK)
            return Response(res_format('submit error', status=Message.ERROR), status=status.HTTP_200_OK)
        else:
            return Response(res_format(serializer.errors, status=Message.ERROR), status=status.HTTP_200_OK)


class RejudgeAPI(APIView):

    def post(self, request, submission_id, *args, **kwargs):
        if request.user is None or request.user.is_authenticated is False:
            return Response(res_format('Login required', status=Message.ERROR), status=status.HTTP_200_OK)
        try:
            submission = Submission.objects.get(id=submission_id)
            if submission.status in {config.Result.Status.STATUS_NO_ACCOUNT.value,
                                     config.Result.Status.STATUS_NETWORK_ERROR.value}:
                submission.status = config.Result.Status.STATUS_PENDING.value
                submission.save()
                submit_task.delay(submission_id)
                return Response(res_format('rejudge submit success'), status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(res_format('System error', status=Message.ERROR), status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(res_format('rejudge failed', status=Message.ERROR), status=status.HTTP_200_OK)
