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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AdminProblemSerializer(queryset, many=True)
        return Response(Message.success(data=serializer.data))

    def create(self, request, *args, **kwargs):
        serializer = AdminProblemSerializer(data=request.data)
        if serializer.is_valid():
            problem = serializer.save()
            return Response(Message.success(data=problem))
        else:
            return Response(Message.error(msg=serializer.errors))

    def retrieve(self, request, pk=None, *args, **kwargs):
        serializer = AdminProblemSerializer(self.get_object())
        return Response(Message.success(data=serializer.data))

    def update(self, request, pk=None, *args, **kwargs):
        serializer = AdminProblemSerializer(instance=self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            problem = serializer.save()
            return Response(Message.success(data=problem))
        else:
            return Response(Message.error(msg=serializer.errors))

    def destroy(self, request, pk=None, *args, **kwargs):
        problem = self.get_object()
        problem.delete()
        return Response(Message.success(msg='Succeed delete'))
