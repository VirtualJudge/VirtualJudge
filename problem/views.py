from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Problem
from .serializers import ProblemSerializer


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]{32}'

    def get_queryset(self):
        return Problem.objects.all()

    serializer_class = ProblemSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProblemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        problem = get_object_or_404(queryset, pk=pk)
        serializer = ProblemSerializer(problem)
        return Response(serializer.data)
