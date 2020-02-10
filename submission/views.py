from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from submission.models import Submission
from submission.serializers import SubmissionAuthorizedSerializer, SubmissionSerializer, SubmissionCreateSerializer


# Create your views here.


class SubmissionViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = SubmissionCreateSerializer(request.data)
            if serializer.is_valid():
                serializer.save(request=request)
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        obj = self.get_object()
        if obj.user == request.user:
            return Response(SubmissionAuthorizedSerializer(obj).data)
        else:
            return Response(SubmissionSerializer(obj).data)
