from rest_framework import serializers

from remote.models import Language


class RemoteLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('oj_language', 'oj_language_name')

