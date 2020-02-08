import re

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from rest_framework import serializers
from rest_framework.serializers import CharField, ValidationError, EmailField

from user.models import Profile


class PasswordSerializer(serializers.Serializer):
    username = CharField()
    old_password = CharField()
    new_password = CharField()
    email = EmailField()

    @staticmethod
    def validate_new_password(value):
        if re.match(r'^[a-zA-Z0-9\-_.]{8,30}$', value) is None:
            raise ValidationError(
                'Password can only contain letters, numbers, -, _ and no shorter than 8 and no longer than 30')
        return value

    def save(self):
        try:
            if len(Profile.objects.filter(username=self.validated_data['username'])) == 1:
                user = Profile.objects.get(username=self.validated_data['username'])
                user.set_password(self.validated_data['new_password'])
                user.email = self.validated_data['email']
                user.save()
                return user
            return None
        except DatabaseError:
            return None


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'username', 'nickname', 'email', 'is_admin')


class LoginSerializer(serializers.Serializer):
    username = CharField()
    password = CharField()

    @staticmethod
    def validate_username(value):
        if re.match(r'^[a-zA-Z0-9\-_]{4,20}$', value) is None:
            raise ValidationError(
                'Username can only contain letters, numbers, -, _ and no shorter than 4 and no longer than 20')
        return value

    @staticmethod
    def validate_password(value):
        if re.match(r'^[a-zA-Z0-9\-_.]{8,30}$', value) is None:
            raise ValidationError(
                'Password can only contain letters, numbers, -, _ and no shorter than 8 and no longer than 30')
        return value

    def login(self, request):
        user = auth.authenticate(username=self.validated_data['username'],
                                 password=self.validated_data['password'])
        if user:
            if request:
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
            user = Profile.objects.create_user(username=username,
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
                'Username can only contain letters, numbers, -, _ and no shorter than 4 and no longer than 20')
        try:
            Profile.objects.get(username=value)
            raise ValidationError('Username exist')
        except ObjectDoesNotExist:
            pass
        return value

    @staticmethod
    def validate_password(value):
        if re.match(r'^[a-zA-Z0-9\-_.]{8,30}$', value) is None:
            raise ValidationError(
                'Password can only contain letters, numbers, -, _ and no shorter than 8 and no longer than 30')
        return value

    @staticmethod
    def validate_email(value):
        if len(value) > 256:
            raise ValidationError('Email address is too long')
        try:
            Profile.objects.get(email=value)
            raise ValidationError('Email address has been registered')
        except ObjectDoesNotExist:
            pass
        return value
