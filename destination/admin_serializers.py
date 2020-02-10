from rest_framework.serializers import ModelSerializer
from destination.models import Language, Platform


class AdminPlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class AdminLanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
