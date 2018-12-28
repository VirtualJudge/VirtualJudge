from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ValidationError, CharField, BooleanField

from support.models import Language, Account, Support


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('oj_name', 'oj_language', 'oj_language_name')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('oj_name', 'oj_username', 'oj_password', 'update_time', 'cookies')


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ('oj_name', 'oj_proxies', 'oj_enable', 'oj_status', 'oj_reuse')


class UpdateProxiesSerializer(serializers.Serializer):
    platform = CharField()
    url = CharField(allow_blank=True, allow_null=True)

    def validate_platform(self, value):
        if Support.objects.filter(oj_name=value):
            return value
        else:
            raise ValidationError(str(value) + ' is not support')

    def save(self, **kwargs):
        try:
            Support.objects.filter(oj_name=self.validated_data['platform']).update(
                oj_proxies=self.validated_data['url'])
        except:
            return False
        return True


class UpdateReuseSerializer(serializers.Serializer):
    platform = CharField()
    reuse = BooleanField()

    def validate_platform(self, value):
        if Support.objects.filter(oj_name=value):
            return value
        else:
            raise ValidationError(str(value) + ' is not support')

    def save(self, **kwargs):
        try:
            Support.objects.filter(Q(oj_name=self.validated_data['platform'])).update(
                oj_reuse=self.validated_data['reuse'])
        except:
            return False
        return True


class UpdateEnableSerializer(serializers.Serializer):
    platform = CharField()
    enable = BooleanField()

    def validate_platform(self, value):
        if Support.objects.filter(oj_name=value):
            return value
        else:
            raise ValidationError(str(value) + ' is not support')

    def save(self, **kwargs):
        try:
            Support.objects.filter(Q(oj_name=self.validated_data['platform'])).update(
                oj_enable=self.validated_data['enable'])
        except:
            return False
        return True
