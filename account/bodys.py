import re

from utils.bodys import JsonValidationError
from utils import bodys


class UsernameField(bodys.BaseField):
    def validate(self, value):
        if not re.match(r'^[a-zA-Z0-9\-_]{4,20}$', value):
            raise JsonValidationError('Password only contains number,letter,_,- and length between 4 and 20.')


class PasswordField(bodys.BaseField):
    def validate(self, value):
        if not re.match(r'^[a-zA-Z0-9\-_.]{6,30}$', value):
            raise JsonValidationError('Password only contains number,letter,_,-,. and length between 6 and 30.')


class EmailField(bodys.BaseField):
    def validate(self, value):
        if not re.match(r'^[A-Za-z0-9\-_.]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', value) or len(value) > 256:
            raise JsonValidationError('Email not valid')


class LoginBody(bodys.Body):
    username = UsernameField()
    password = PasswordField()


class RegisterBody(bodys.Body):
    username = UsernameField()
    password = PasswordField()
    email = EmailField()
