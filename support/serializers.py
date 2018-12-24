from spider.core import Core
from rest_framework import serializers
from rest_framework.serializers import ValidationError, CharField

from support.models import Language, Account, Support
from django.db import DatabaseError
from support.tasks import update_oj_status


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
        if Core.is_support(value) is False:
            raise ValidationError(str(value) + ' is not support')
        return value

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
            support = Support.objects.filter(oj_name=self.validated_data['remote_oj'])
            if support.count() == 1:
                oj = Support.objects.get(oj_name=self.validated_data['remote_oj'])
                if oj.oj_status == 'PENDING':
                    update_oj_status.delay(oj.oj_name)
            elif support.count() == 0:
                Support.objects.create(oj_name=self.validated_data['remote_oj']).save()
                oj = Support.objects.get(oj_name=self.validated_data['remote_oj'])
                if oj.oj_status == 'PENDING':
                    update_oj_status.delay(oj.oj_name)
            return True
        except DatabaseError as e:
            print(e)
            return False
