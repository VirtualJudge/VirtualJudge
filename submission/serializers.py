from rest_framework import serializers
from submission.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'problem_id', 'contest_id', 'code', 'language', 'remote_oj', 'remote_id')


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'remote_oj', 'remote_id', 'verdict', 'execute_time', 'execute_memory')
