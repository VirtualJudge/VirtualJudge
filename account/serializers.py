import re

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework import serializers
from rest_framework.serializers import CharField, ValidationError, EmailField

from account.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username',)


class LoginSerializer(serializers.Serializer):
    username = CharField()
    password = CharField()

    @staticmethod
    def validate_username(value):
        if re.match(r'^[a-zA-Z0-9\-_]{4,20}$', value) is None:
            raise ValidationError(
                'Username only contains number,letter,_,- '
                'and length between 4 and 20.')
        return value

    @staticmethod
    def validate_password(value):
        if re.match(r'^[a-zA-Z0-9\-_.]{8,30}$', value) is None:
            raise ValidationError(
                'Password only contains number,letter,_,-,. '
                'and length between 8 and 30.')
        return value

    def login(self, request):
        user = auth.authenticate(username=self.validated_data['username'],
                                 password=self.validated_data['password'])
        if user:
            auth.login(request, user)
            return user


class RegisterSerializer(serializers.Serializer):
    username = CharField()
    password = CharField()
    email = EmailField()

    def save(self, **kwargs):
        email = self.validated_data['email']
        password = self.validated_data['password']
        username = self.validated_data['username']
        try:
            user = UserProfile.objects.create_user(username=username,
                                                   password=password,
                                                   email=email)
            user.save()
            return True
        except DatabaseError:
            return False

    @staticmethod
    def validate_username(value):
        if re.match(r'^[a-zA-Z0-9\-_]{4,20}$', value) is None:
            raise ValidationError(
                'Username only contains number,letter,_,- '
                'and length between 4 and 20.')
        try:
            UserProfile.objects.get(username=value)
            raise ValidationError('Username exist')
        except ObjectDoesNotExist:
            pass
        return value

    @staticmethod
    def validate_password(value):
        if re.match(r'^[a-zA-Z0-9\-_.]{6,30}$', value) is None:
            raise ValidationError(
                'Password only contains number,letter,_,-,. '
                'and length between 6 and 30.')
        return value

    @staticmethod
    def validate_email(value):
        if len(value) > 256:
            raise ValidationError('Email too long')
        try:
            UserProfile.objects.get(email=value)
            raise ValidationError('Email exist')
        except ObjectDoesNotExist:
            pass
        return value
