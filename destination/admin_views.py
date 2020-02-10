from rest_framework.viewsets import ModelViewSet
from destination.admin_serializers import AdminLanguageSerializer, AdminPlatformSerializer
from destination.models import Language, Platform
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from util.message import Message


# Create your views here.

class AdminPlatformViewSet(ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = AdminPlatformSerializer
    permission_classes = [IsAdminUser]


class AdminLanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = AdminLanguageSerializer
    permission_classes = [IsAdminUser]
