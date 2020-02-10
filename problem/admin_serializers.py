from rest_framework import serializers
from problem.models import Problem


class AdminProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        read_only_fields = ['id', 'index', 'update_time', 'platform']
