from rest_framework import serializers
from submission.models import Submission


class VerdictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'remote_oj', 'remote_id', 'verdict_status',
                  'verdict', 'execute_time', 'execute_memory', 'status')


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'problem_id', 'token', 'contest_id', 'code', 'language', 'remote_oj', 'remote_id', 'status')


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'remote_oj', 'token', 'remote_id', 'verdict', 'execute_time', 'execute_memory', 'status')
