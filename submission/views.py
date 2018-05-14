from datetime import datetime

from VirtualJudgeSpider import config
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework import status
from rest_framework.views import APIView, Response
from account.models import UserProfile
from submission.models import Submission
from submission.serializers import SubmissionListSerializer, VerdictSerializer, SubmissionSerializer
from submission.tasks import submit_task
from utils.response import res_format, Message
from django.db.models import F


class VerdictAPI(APIView):
    def post(self, request, submission_id, *args, **kwargs):
        try:
            submission = Submission.objects.get(id=submission_id)
            return Response(res_format(VerdictSerializer(submission).data), status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(res_format('submission not exist', status=Message.ERROR),
                            status=status.HTTP_200_OK)


class SubmissionAPI(APIView):

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
                if submission.status != config.Result.Status.STATUS_PENDING:
                    return Response(res_format(submission.id), status=status.HTTP_200_OK)
                try:
                    UserProfile.objects.filter(username=request.user).update(submitted=F('submitted') + 1)
                    if len(Submission.objects.filter(user=str(request.user),
                                                     remote_oj=serializer.validated_data['remote_oj'],
                                                     remote_id=serializer.validated_data['remote_id'])) == 1:
                        print('update attempted:' + str(request.user))
                        UserProfile.objects.filter(username=str(request.user)).update(attempted=F('attempted') + 1)

                except DatabaseError:
                    import traceback
                    traceback.print_exc()
                    pass
                submit_task.delay(submission.id)
                return Response(res_format(submission.id), status=status.HTTP_200_OK)
            return Response(res_format('submit error', status=Message.ERROR), status=status.HTTP_200_OK)
        else:
            return Response(res_format(serializer.errors, status=Message.ERROR), status=status.HTTP_200_OK)


class SubmissionListAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            submissions = Submission.objects.filter(contest_id=None).order_by('-create_time')[:20]
            return Response(res_format(SubmissionListSerializer(submissions, many=True).data),
                            status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(res_format('System error', status=Message.ERROR),
                            status=status.HTTP_200_OK)


class ReJudgeAPI(APIView):

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
            return Response(res_format('System error', status=Message.ERROR),
                            status=status.HTTP_200_OK)
        except DatabaseError:
            return Response(res_format('rejudge failed', status=Message.ERROR), status=status.HTTP_200_OK)
