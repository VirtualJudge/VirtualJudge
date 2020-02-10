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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProblemSerializer(queryset, many=True)
        return Response(Message.success(data=serializer.data))

    def retrieve(self, request, pk=None, *args, **kwargs):
        problem = self.get_object()
        serializer = ProblemSerializer(problem)
        return Response(Message.success(data=serializer.data))
