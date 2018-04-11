import json
import traceback
from json import JSONDecodeError

from utils.bodys import Body, BaseField, JsonValidationError


class AccountField(BaseField):
    def validate(self, value):
        try:
            print(value)
            accounts = json.loads(value)
            for account in accounts:
                if account.get('remote_oj') and account.get('username') and account.get('password'):
                    continue
                raise JsonValidationError('account file not satisfied')
        except JSONDecodeError:
            traceback.print_exc()
            raise JsonValidationError('account file not satisfied')


class AccountBody(Body):
    account = AccountField()
