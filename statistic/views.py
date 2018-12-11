# Create your views here.
from datetime import timedelta, datetime

from django.utils import datetime_safe
from rest_framework import status
from rest_framework.views import APIView, Response

from submission.models import Submission
from utils.response import res_format


class SubmissionAPI(APIView):
    def get(self, request, *args, **kwargs):
        today = datetime.fromisoformat(datetime_safe.datetime.today().strftime("%Y-%m-%d"))
        counts = []
        for offset in range(6, -1, -1):
            counts.append(Submission.objects.filter(create_time__gte=today - timedelta(days=offset),
                                                    create_time__lt=today - timedelta(days=offset - 1)).count())
        return Response(res_format(counts), status=status.HTTP_200_OK)
