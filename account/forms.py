from django import forms
from django.core.exceptions import ValidationError
import re


class UsernameField(forms.CharField):
    def validate(self, value):
        if not re.match(r'^[a-zA-Z0-9\-_]{4,20}$', value):
            raise ValidationError('Password only contains number,letter,_,- and length between 4 and 20.')


class PasswordField(forms.CharField):
    def validate(self, value):
        if not re.match(r'^[a-zA-Z0-9\-_]{6,30}$', value):
            raise ValidationError('Password only contains number,letter,_,- and length between 6 and 30.')


class MyEmailField(forms.CharField):
    def validate(self, value):
        if not re.match(r'^[A-Za-z0-9\-_.]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', value) or len(value) > 256:
            raise ValidationError('Email not valid')


class LoginForm(forms.Form):
    username = UsernameField()
    password = PasswordField()


class RegisterForm(forms.Form):
    username = UsernameField()
    password = PasswordField()
    email = MyEmailField()


class ChangePasswordForm(forms.Form):
    password = PasswordField()


class ChangeEmailForm(forms.Form):
    email = MyEmailField()
