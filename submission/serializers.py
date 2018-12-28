import hashlib

from django.db import DatabaseError
from rest_framework import serializers
from rest_framework.serializers import CharField
from rest_framework.validators import ValidationError

from problem.models import Problem
from submission.models import Submission
from support.models import Language, Support


class VerdictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = (
            'id', 'remote_oj', 'remote_id', 'verdict_info', 'verdict', 'execute_time', 'execute_memory', 'status',
            'reloadable', 'language_name', 'user', 'code', 'create_time')


class SubmissionSerializer(serializers.Serializer):
    code = CharField()
    language = CharField()
    remote_oj = CharField()
    remote_id = CharField()

    def save(self, user):
        """
        在这里可以统计提交量
        :param user: request.user
        :return: submission object
        """
        try:
            language = self.validated_data['language']
            remote_oj = self.validated_data['remote_oj']
            language_obj = Language.objects.get(oj_name=remote_oj, oj_language=language)
            submission = Submission(code=self.validated_data['code'],
                                    user=user,
                                    language=language_obj.oj_language,
                                    language_name=language_obj.oj_language_name,
                                    sha256=hashlib.sha256(self.validated_data['code'].encode('utf-8')).hexdigest(),
                                    remote_id=self.validated_data['remote_id'],
                                    remote_oj=self.validated_data['remote_oj'])

            submission.save()
            return submission
        except DatabaseError:
            import traceback
            traceback.print_exc()
            return None

    def validate_code(self, value):
        if len(value) < 20:
            raise ValidationError('code is too short')
        return value

    def validate_remote_oj(self, remote_oj):
        if remote_oj not in list({item.oj_name for item in Support.objects.filter(oj_enable=True)}):
            raise ValidationError(str(remote_oj) + ' is not supported')
        return remote_oj

    def validate(self, value):
        remote_oj = value['remote_oj']
        remote_id = value['remote_id']
        language = value['language']
        if Problem.objects.filter(remote_oj=remote_oj, remote_id=remote_id).exists() is False:
            raise ValidationError('problem not exist')
        if Language.objects.filter(oj_name=remote_oj, oj_language=language).exists() is False:
            raise ValidationError('language not exist')
        return value


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = (
            'id', 'remote_oj', 'user', 'remote_id', 'language',
            'language_name', 'verdict_info', 'verdict', 'execute_time', 'reloadable',
            'execute_memory', 'create_time', 'status')
