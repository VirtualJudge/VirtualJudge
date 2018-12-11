from rest_framework import serializers
from problem.models import Problem


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = (
            'id', 'remote_id', 'remote_oj', 'update_time', 'title',
            'time_limit', 'memory_limit', 'html', 'request_status')


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'remote_id', 'remote_oj', 'update_time', 'title', 'remote_url')
