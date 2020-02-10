from rest_framework.serializers import ModelSerializer
from submission.models import Submission


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ['problem', 'language', 'submit_time', 'result']


class SubmissionCreateSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ['problem', 'language', 'code']


class SubmissionAuthorizedSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ['user', 'problem', 'language', 'submit_time', 'result', 'code', 'extra_msg']
