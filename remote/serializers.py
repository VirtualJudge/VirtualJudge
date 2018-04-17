from VirtualJudgeSpider import control
from rest_framework import serializers
from rest_framework.serializers import ValidationError, CharField

from remote.models import Language
from django.db import DatabaseError
from remote.models import Account


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('oj_language', 'oj_language_name')


class AccountSerializer(serializers.Serializer):
    remote_oj = CharField()
    username = CharField()
    password = CharField()

    @staticmethod
    def validated_remote_oj(value):
        if control.Controller.is_support(value) is False:
            raise ValidationError(str(value) + ' is not support')
        return control.Controller.get_real_remote_oj(value)

    def validate(self, value):
        self.validated_remote_oj(value['remote_oj'])
        return value

    def save(self, **kwargs):
        try:
            account = Account.objects.filter(oj_name=self.validated_data['remote_oj'],
                                             oj_username=self.validated_data['username'])
            if account:
                account.update(oj_password=self.validated_data['password'])
            else:
                Account(oj_name=self.validated_data['remote_oj'], oj_password=self.validated_data['password'],
                        oj_username=self.validated_data['username']).save()
            return True
        except DatabaseError:
            return False
