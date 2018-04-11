import re

from utils.bodys import JsonValidationError
from utils import bodys


class UsernameField(bodys.BaseField):
    def validate(self, value):
        print(value)
        if re.match(r'^[a-zA-Z0-9\-_]{4,20}$', value) is None:
            raise JsonValidationError('Username only contains number,letter,_,- and length between 4 and 20.')


class PasswordField(bodys.BaseField):
    def validate(self, value):
        if re.match(r'^[a-zA-Z0-9\-_.]{6,30}$', value) is None:
            print(value, len(value))
            raise JsonValidationError('Password only contains number,letter,_,-,. and length between 6 and 30.')


class EmailField(bodys.BaseField):
    def validate(self, value):
        print(value)
        print(re.match(r'^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$', value))
        if re.match(r'^[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$', value) is None:
            raise JsonValidationError('Email is not valid')
        if len(value) > 256:
            raise JsonValidationError('Email too long')


class LoginBody(bodys.Body):
    username = UsernameField()
    password = PasswordField()


class RegisterBody(bodys.Body):
    username = UsernameField()
    password = PasswordField()
    email = EmailField()
