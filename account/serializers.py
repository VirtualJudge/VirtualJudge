from rest_framework import serializers
from account.models import UserProfile
from rest_framework.serializers import CharField, ValidationError, EmailField
import re
from account.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username',)


class LoginSerializer(serializers.Serializer):
    username = CharField()
    password = CharField()

    def validate_username(self, value):
        if re.match(r'^[a-zA-Z0-9\-_]{4,20}$', value) is None:
            raise ValidationError('Username only contains number,letter,_,- and length between 4 and 20.')
        try:
            UserProfile.objects.get(username=value)
        except ObjectDoesNotExist:
            raise ValidationError('Username not exist')
        return value

    def validate_password(self, value):
        if re.match(r'^[a-zA-Z0-9\-_.]{8,30}$', value) is None:
            raise ValidationError('Password only contains number,letter,_,-,. and length between 8 and 30.')
        return value


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'email')

    def save(self, **kwargs):
        email = self.validated_data['email']
        password = self.validated_data['password']
        username = self.validated_data['username']
        user = UserProfile.objects.create_user(username=username, password=password, email=email)
        user.save()

    def validate_username(self, value):
        if re.match(r'^[a-zA-Z0-9\-_]{4,20}$', value) is None:
            raise ValidationError('Username only contains number,letter,_,- and length between 4 and 20.')
        try:
            UserProfile.objects.get(username=value)
            raise ValidationError('Username exist')
        except ObjectDoesNotExist:
            pass
        return value

    def validate_password(self, value):
        if re.match(r'^[a-zA-Z0-9\-_.]{6,30}$', value) is None:
            raise ValidationError('Password only contains number,letter,_,-,. and length between 6 and 30.')
        return value

    def validate_email(self, value):
        if re.match(r'^[-_\w.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}$', value) is None:
            raise ValidationError('Email is not valid')
        if len(value) > 256:
            raise ValidationError('Email too long')
        try:
            UserProfile.objects.get(email=value)
            raise ValidationError('Email exist')
        except ObjectDoesNotExist:
            pass
        return value
