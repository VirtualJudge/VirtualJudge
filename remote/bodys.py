from utils.bodys import Body, BaseField, JsonValidationError
import json
from json import JSONDecodeError
from VirtualJudgeSpider import Control


class AccountField(BaseField):
    def validate(self, value):
        try:
            accounts = json.loads(value)
            for account in accounts:
                if account.get('remote_oj') and account.get('username') and account.get('password'):
                    continue
                raise JsonValidationError('account file not satisfied')
        except JSONDecodeError:
            raise JsonValidationError('account file not satisfied')


class AccountBody(Body):
    account = AccountField()
