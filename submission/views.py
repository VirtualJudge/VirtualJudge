from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from utils.permissions import is_authenticated
from submission.tasks import run_submission_task
from user.models import Activity
from utils.response import msg
from .models import Submission
from .serializers import SubmissionSerializer, SubmissionShortSerializer, SubmissionCreateSerializer, \
    SubmissionUpdateSerializer


class SubmissionFilter(filters.FilterSet):
    verdict = filters.CharFilter(field_name='verdict', lookup_expr='iexact')
    user = filters.CharFilter(field_name='user', lookup_expr='exact')
    username = filters.CharFilter(field_name='user__username', lookup_expr='contains')
    problem_id = filters.CharFilter(field_name='problem__id', lookup_expr='icontains')
    language = filters.CharFilter(field_name='lang', lookup_expr='exact')
    problem_remote_oj = filters.CharFilter(field_name='problem__remote_oj', lookup_expr='icontains')
    problem_remote_id = filters.CharFilter(field_name='problem__remote_id', lookup_expr='icontains')

    class Meta:
        model = Submission
        fields = ['verdict', 'user', 'username', 'problem_id', 'problem_remote_oj', 'problem_remote_id', 'language']


class SubmissionViewSet(viewsets.GenericViewSet, UpdateModelMixin):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filterset_class = SubmissionFilter
    lookup_value_regex = r'\d+'

    @is_authenticated()
    def create(self, request: Request):
        last_submit_time = request.user.last_submit_time
        if last_submit_time is not None and timezone.now() < last_submit_time + timedelta(seconds=10):
            return Response(msg(err=_('Can\'t submit twice within 10 seconds.')))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save(user=request.user)
        run_submission_task.apply_async(
            args=[submission.id,
                  submission.problem.id,
                  submission.problem.manifest,
                  submission.code,
                  submission.lang,
                  submission.problem.time_limit,
                  submission.problem.memory_limit], queue='judge')
        Activity(user=request.user, category=Activity.SUBMISSION,
                 info=f'用户提交了题目{submission.problem.id}，提交编号是{submission.id}').save()
        return Response(msg(SubmissionShortSerializer(submission).data))

    def list(self, request: Request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @is_authenticated()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 权限检查，管理员或者作者用户
        if not request.user.is_staff and request.user.id != instance.user.id:
            raise PermissionDenied

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(msg(_('Success')))

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        submission = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(submission)
        return Response(msg(serializer.data))

    @action(detail=True, methods=['get'])
    def personal(self, request, pk=None):
        queryset = self.get_queryset()
        submission = get_object_or_404(queryset, pk=pk)
        if submission.user == request.user or request.user.is_staff or submission.is_public:
            serializer = self.get_serializer(submission)
            return Response(msg(serializer.data))
        raise PermissionDenied

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SubmissionShortSerializer
        elif self.action == 'create':
            return SubmissionCreateSerializer
        elif self.action == 'update':
            return SubmissionUpdateSerializer
        else:
            return self.serializer_class
