from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ContestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    problems = serializers.ListField(child=serializers.IntegerField(), max_length=30)
    password = serializers.CharField(max_length=20, required=False)

    def validate_title(self, value):
        return value

    def validate_start_time(self, value):
        if value < timezone.now():
            raise ValidationError('Start time must not be earlier than now')
        return value

    def validate_end_time(self, value):
        return value

    def validate_problems(self, value):
        return value

    def validate_password(self, value):
        return value

    def validate(self, value):
        return value

    def save(self, user):
        return True
