from rest_framework import serializers

from problem.models import Problem


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id',
                  'title',
                  'last_update',
                  'remote_oj',
                  'remote_id']
        depth = 0


class ProblemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id',
                  'title',
                  'content',
                  'time_limit',
                  'memory_limit',
                  'remote_oj',
                  'remote_id']

    def save(self):
        if Problem.objects.filter(remote_id=self.validated_data['remote_id'],
                                  remote_oj=self.validated_data['remote_oj']).exists():
            return False
        Problem(title=self.validated_data['title'],
                content=self.validated_data['content'],
                time_limit=self.validated_data['time_limit'],
                memory_limit=self.validated_data['memory_limit'],
                remote_oj=self.validated_data['remote_oj'],
                remote_id=self.validated_data['remote_id']).save()
        return True


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id',
                  'title',
                  'content',
                  'time_limit',
                  'memory_limit',
                  'last_update',
                  'remote_oj',
                  'remote_id']
        depth = 0
