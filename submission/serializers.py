from rest_framework import serializers

from problem.serializers import ProblemListSerializer
from user.models import User
from user.serializers import UserShortSerializer
from .models import Submission


# list submission serializer
class SubmissionShortSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    problem = ProblemListSerializer()

    class Meta:
        model = Submission
        fields = (
            'id',
            'user',
            'problem',
            'create_time',
            'verdict',
            'lang',
            'time_cost',
            'memory_cost',
            'is_public',
            'remote_verdict'
        )


class SubmissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'is_public')


# basic submission serializer
class SubmissionSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    problem = ProblemListSerializer()

    class Meta:
        model = Submission
        fields = (
            'id',
            'user',
            'code',
            'problem',
            'verdict',
            'lang',
            'create_time',
            'time_cost',
            'memory_cost',
            'additional_info',
            'is_public',
            'remote_verdict'
        )


# create submission serializer
class SubmissionCreateSerializer(serializers.ModelSerializer):
    lang = serializers.CharField()
    code = serializers.CharField(max_length=65536)

    class Meta:
        model = Submission
        fields = (
            'code',
            'problem',
            'lang',
        )

    def save(self, user: User):
        submission = Submission(
            user=user,
            code=self.validated_data['code'],
            problem=self.validated_data['problem'],
            lang=self.validated_data['lang'],
        )
        submission.save()
        return submission
