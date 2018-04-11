from rest_framework import serializers

from config.models import RemoteLanguage


class RemoteLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteLanguage
        fields = ('oj_language', 'oj_language_name')

