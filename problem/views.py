from rest_framework import viewsets
from rest_framework.response import Response

from util.message import Message
from .models import Problem
from .serializers import ProblemSerializer


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
