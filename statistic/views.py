# Create your views here.
from datetime import timedelta

from django.utils import datetime_safe
from rest_framework import status
from rest_framework.views import APIView, Response

from submission.models import Submission
from utils.response import res_format


class SubmissionAPI(APIView):
    def get(self, request, *args, **kwargs):
        today = datetime_safe.datetime.today()
        counts = []
        for offset in range(7, 0, -1):
            try:
                counts.append(Submission.objects.filter(create_time__gte=today - timedelta(days=offset),
                                                        create_time__lt=today - timedelta(days=offset - 1)).count())
            except Exception as e:
                print(e)
                counts.append(0)
        return Response(res_format(counts), status=status.HTTP_200_OK)
