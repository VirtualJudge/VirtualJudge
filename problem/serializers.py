from rest_framework import serializers
from problem.models import Problem


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = (
            'id', 'remote_id', 'remote_oj', 'remote_url', 'update_time', 'title',
            'time_limit', 'memory_limit', 'html', 'retry_count', 'request_status')


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'remote_id', 'remote_oj', 'remote_url', 'update_time', 'title')
