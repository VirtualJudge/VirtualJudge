import re

from VirtualJudgeSpider.Control import Controller

from remote.models import Language
from utils.bodys import BaseField, Body, JsonValidationError
from contest.models import Contest


class RemoteOJField(BaseField):
    def validate(self, value):
        if not Controller.is_support(value):
            raise JsonValidationError('remote online judge not support')


class RemoteIdField(BaseField):
    def validate(self, value):
        if not re.match(r'^[a-zA-Z0-9_]{1,10}$', value):
            raise JsonValidationError('problem id is not valid')


class SourceCodeField(BaseField):
    def validate(self, value):
        if len(value) > 1024 * 1024:
            raise JsonValidationError('code is too long')


class LanguageField(BaseField):
    def validate(self, value):
        try:
            if Language.objects.filter(oj_language=value) is None:
                raise JsonValidationError('Language not support')
        except:
            raise JsonValidationError('Language not support')


class ContestIdField(BaseField):
    def validate(self, value):
        try:
            if type(value) != int:
                raise JsonValidationError('Integer contest id required')
            if value is not None:
                Contest.objects.get(id=value)
        except:
            raise JsonValidationError('Contest not exist')


class SubmissionBody(Body):
    remote_oj = RemoteOJField()
    remote_id = RemoteIdField()
    source_code = SourceCodeField()
    language = LanguageField()
