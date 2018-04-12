from VirtualJudgeSpider import Control
from rest_framework import serializers
from rest_framework.serializers import ValidationError, CharField

from remote.models import Language


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('oj_language', 'oj_language_name')


class AccountSerializer(serializers.Serializer):
    remote_oj = CharField()
    username = CharField()
    password = CharField()

    def validated_remote_oj(self, value):
        if Control.Controller.is_support(value) is False:
            raise ValidationError(str(value) + ' is not support')
        return Control.Controller.get_real_remote_oj(value)

    def validate(self, value):
        self.validated_remote_oj(value['remote_oj'])
        return value
