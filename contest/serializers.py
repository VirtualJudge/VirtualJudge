from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from contest.models import Contest
from django.contrib.postgres.fields import JSONField
from VirtualJudgeSpider import control
from problem.models import Problem


class ContestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    problems = serializers.ListField(child=JSONField(), max_length=30)
    password = serializers.CharField(max_length=20, required=False)

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

    @staticmethod
    def validate_problems(values):
        for value in values:
            if value.get('remote_oj') is None or value.get('remote_id') is None:
                raise ValidationError('Problem not valid')
            if control.Controller.is_support(value.get('remote_oj')) is False:
                raise ValidationError('Remote OJ not valid' + str(value.get('remote_oj')))
            if Problem.objects.filter(remote_oj=value.get('remote_oj'),
                                      remote_id=value.get('remote_id')).exists() is False:
                raise ValidationError(
                    'Problem not exist:' + str(value.get('remote_oj')) + ':' + str(value.get('remote_id')))
        return values

    @staticmethod
    def validate_password(value):
        return value

    def validate(self, value):
        if value['start_time'] > value['end_time']:
            raise ValidationError('End time must not be earlier than start time')
        return value

    def save(self, user):
        if user is None or user.is_authenticated is False:
            return None
        if self.validated_data['password'] is None:
            contest = Contest(title=self.validated_data['title'], start_time=self.validated_data['start_time'],
                              user=str(user),
                              end_time=self.validated_data['end_time'], problems=self.validated_data['problems'])
            contest.save()
            return contest
        else:
            contest = Contest(title=self.validated_data['title'],
                              start_time=self.validated_data['start_time'],
                              password=self.validated_data['password'],
                              user=str(user),
                              end_time=self.validated_data['end_time'],
                              problems=self.validated_data['problems'])
            contest.save()
            return contest


class ContestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'title', 'user', 'start_time', 'end_time')