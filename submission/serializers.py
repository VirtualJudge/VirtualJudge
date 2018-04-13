from django.db import DatabaseError
from rest_framework import serializers
from rest_framework.serializers import CharField
from rest_framework.serializers import IntegerField
from rest_framework.validators import ValidationError

from contest.models import Contest
from problem.models import Problem
from remote.models import Language
from submission.models import Submission


class VerdictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = (
            'id', 'remote_oj', 'remote_id', 'verdict_status', 'verdict', 'execute_time', 'execute_memory', 'status')


class SubmissionSerializer(serializers.Serializer):
    contest_id = IntegerField(required=False)
    code = CharField()
    language = CharField()
    remote_oj = CharField()
    remote_id = CharField()

    def save(self, user):
        try:
            submission = Submission(contest_id=self.contest_id, code=self.code, user=user, language=self.language,
                                    remote_id=self.remote_id, remote_oj=self.remote_oj)
            submission.save()
            return submission.id
        except DatabaseError:
            return None

    def validate_contest_id(self, contest_id):
        try:
            if Contest.objects.filter(id=contest_id).exists() is False:
                raise ValidationError('contest is not exist')
        except DatabaseError:
            raise ValidationError('system error')
        return contest_id

    def validate_code(self, value):
        return value

    def validate_remote_oj(self, remote_oj):
        if Language.objects.filter(oj_name=remote_oj).exists() is False:
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
        fields = ('id', 'remote_oj', 'user', 'remote_id', 'verdict', 'execute_time', 'execute_memory', 'status')
