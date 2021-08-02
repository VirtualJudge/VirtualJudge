from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.views import Response

from problem.models import Problem
from problem.serializers import ProblemSerializer, ProblemListSerializer
from utils.response import msg


# Create your views here.
class ProblemFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    remote_oj = filters.CharFilter(field_name='remote_oj', lookup_expr='icontains')
    remote_id = filters.CharFilter(field_name='remote_id', lookup_expr='icontains')

    class Meta:
        model = Problem
        fields = ['id', 'title', 'remote_oj', 'remote_id']


class ProblemViewSet(viewsets.GenericViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filterset_class = ProblemFilter
    lookup_value_regex = r'\d+'

    def list(self, request, *args, **kwargs):
        """
        管理员的话，返回所有题目列表
        普通登录的话，返回可以查看的，或者自己上传的题目列表
        未登录的话，仅返回可以查看的题目列表
        :param request: Request
        :param args:
        :param kwargs:
        :return: Response
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        problem = self.get_object()
        serializer = ProblemSerializer(problem)
        return Response(msg(serializer.data))

    def get_serializer_class(self):
        if self.action == 'list':
            return ProblemListSerializer
        else:
            return self.serializer_class
