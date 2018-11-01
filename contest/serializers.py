from django.db import DatabaseError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from contest.models import Contest
from contest.models import ContestProblem


class ContestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    problems = serializers.ListField()

    @staticmethod
    def validate_title(value):
        return value

    def validate(self, value):
        return value

    def validate_problems(self, value):
        if isinstance(value, list) is False:
            raise ValidationError(f'value required {type(list)}, but got {type(value)}')
        if len(value) > 100:
            raise ValidationError(f'value length > 100')
        for item in value:
            if item.get('remote_oj') is None or item.get('remote_id') is None:
                raise ValidationError('lack information')
        return value

    def save(self, user):
        if user is None or user.is_authenticated is False:
            return None
        try:
            contest = Contest(title=self.validated_data['title'], user=str(user))
            contest.save()
            contest_problem_list = [ContestProblem(remote_id=problem['remote_id'],
                                                   remote_oj=problem['remote_oj'],
                                                   contest_id=contest.id) for problem in
                                    self.validated_data['problems']]
            ContestProblem.objects.bulk_create(contest_problem_list)
            return contest
        except DatabaseError:
            return None


class ContestProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContestProblem
        fields = ('remote_oj', 'remote_id', 'alias')


class ContestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'title', 'user', 'created_time')
