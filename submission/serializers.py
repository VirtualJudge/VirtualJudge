from rest_framework import serializers
from submission.models import Submission

from rest_framework.serializers import CharField
from rest_framework.serializers import IntegerField
from rest_framework.validators import ValidationError
from django.db import DatabaseError


class VerdictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = (
            'id', 'remote_oj', 'remote_id', 'verdict_status', 'verdict', 'execute_time', 'execute_memory', 'status')


class SubmissionSerializer(serializers.ModelSerializer):
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

    def validate_contest_id(self, value):
        pass

    def validate_code(self, value):
        pass

    def validate_language(self, value):
        pass

    def validate_remote_oj(self, value):
        pass

    def validate_remote_id(self, value):
        pass

    def validate(self, value):
        if value.get('contest_id'):
            self.validate_code(value['contest_id'])
        self.validate_code(value['code'])
        self.validate_code(value['language'])
        self.validate_code(value['remote_id'])
        self.validate_code(value['remote_oj'])
        return value


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'remote_oj', 'user', 'remote_id', 'verdict', 'execute_time', 'execute_memory', 'status')
