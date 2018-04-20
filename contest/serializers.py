from django.db import DatabaseError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from contest.models import Contest
from contest.models import ContestProblem


class ContestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    problems = serializers.JSONField(binary=True)

    @staticmethod
    def validate_title(value):
        return value

    @staticmethod
    def validate_start_time(value):
        if value < timezone.now():
            raise ValidationError('Start time must not be earlier than now')
        return value

    @staticmethod
    def validate_end_time(value):
        if value < timezone.now():
            raise ValidationError('End time must not be earlier than now')
        return value

    def validate(self, value):
        if value['start_time'] > value['end_time']:
            raise ValidationError('End time must not be earlier than start time')
        return value

    def validate_problems(self, value):
        if isinstance(value, list) is False:
            raise ValidationError(f'value required {type(list)}, but got {type(value)}')
        for item in value:
            if item.get('remote_oj') is None or item.get('remote_id') is None:
                raise ValidationError('lack information')
        return value

    def save(self, user):
        if user is None or user.is_authenticated is False:
            return None
        try:
            print(self.validated_data['start_time'])
            print(self.validated_data['end_time'])
            contest = Contest(title=self.validated_data['title'],
                              start_time=self.validated_data['start_time'],
                              user=str(user),
                              end_time=self.validated_data['end_time'])
            contest.save()
            print(contest.start_time, contest.end_time)
            contest_problem_list = [ContestProblem(remote_id=problem['remote_id'],
                                                   remote_oj=problem['remote_oj'],
                                                   contest_id=contest.id) for problem in
                                    self.validated_data['problems']]
            ContestProblem.objects.bulk_create(contest_problem_list)
            return contest
        except DatabaseError:
            return None


class ContestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'title', 'user', 'start_time', 'end_time', 'created_time')
