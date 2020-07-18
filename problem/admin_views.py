from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from problem.models import Problem
from problem.admin_serializers import AdminProblemSerializer
from util.message import Message


class AdminProblemViewSet(ModelViewSet):
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'
    permission_classes = [IsAdminUser]
    queryset = Problem.objects.all()

    serializer_class = AdminProblemSerializer
