import random
import re
from hashlib import md5

from django.contrib import auth
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from rest_framework import serializers

from vj.settings import ACTIVATE_CODE_AGE
from user.models import User, Activity, StudentInfo
from user.utils import USERNAME_PATTERN, PASSWORD_PATTERN
from utils.views import CaptchaAPI


class StudentInfoShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = ['id', 'school']


class PermissionListField(serializers.RelatedField):
    def to_representation(self, value: Permission):
        return {
            'id': value.id,
            'name': f'{value.content_type.app_label}.{value.codename}'
        }


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['username']


class AdvancedUserInfoSerializer(serializers.ModelSerializer):
    user_permissions = PermissionListField(read_only=True, many=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_superuser',
            # 'total_passed',
            # 'total_accepted',
            # 'total_submitted',
            'activated',
            'ban',
            'user_permissions']


class UserInfoSerializer(serializers.ModelSerializer):
    user_permissions = PermissionListField(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_superuser',
            'total_passed',
            'total_accepted',
            'total_submitted',
            'activated',
            'user_permissions']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    captcha = serializers.CharField()

    def validate_captcha(self, value):
        request = self.context['request']
        if not CaptchaAPI.verify_captcha(request, value):
            raise serializers.ValidationError(_('Captcha verify error.'))
        return value

    @staticmethod
    def validate_username(value):
        if re.match(USERNAME_PATTERN, value) is None:
            raise serializers.ValidationError(
                _('Username can only contain letters, numbers, -, _ and no shorter than 6 and no longer than 20'))
        return value

    @staticmethod
    def validate_password(value):
        if re.match(PASSWORD_PATTERN, value) is None:
            raise serializers.ValidationError(
                _('Password can only contain letters, numbers, -, _ and no shorter than 8 and no longer than 20'))
        return value

    def validate(self, data):
        user = auth.authenticate(username=data['username'],
                                 password=data['password'])
        if not user:
            raise serializers.ValidationError(_('Username or password wrong'))
        return data

    def login(self, request):
        user = auth.authenticate(username=self.validated_data['username'],
                                 password=self.validated_data['password'])
        if user.ban:
            raise Exception(_('You have been banned from this website.'))
        elif user.activated:
            auth.login(request, user)
            user.save()
            Activity.objects.create(user=user, category=Activity.USER_LOGIN, info='登录成功')
            return user
        else:
            raise Exception(_('Account not activated.'))


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField(max_length=100)
    verify_code = serializers.CharField()

    def save(self, **kwargs):
        email = self.validated_data['email']
        password = self.validated_data['password']
        username = self.validated_data['username']

        user = User.objects.create_user(username=username,
                                        password=password,
                                        activated=True,
                                        email=email)
        return user

    def validate(self, data):
        email = str(data['email']).encode('utf-8')
        if cache.get(f'check-email-code-{md5(email).hexdigest()}') != data['verify_code']:
            raise serializers.ValidationError(_('Email verify code error'))
        return data

    @staticmethod
    def validate_username(value):
        if re.match(USERNAME_PATTERN, value) is None:
            raise serializers.ValidationError(
                _('Username can only contain letters, numbers, -, _ and no shorter than 6 and no longer than 20'))
        try:
            User.objects.get(username=value)
            raise serializers.ValidationError(_('Username exist'))
        except ObjectDoesNotExist:
            pass
        return value

    @staticmethod
    def validate_password(value):
        if re.match(PASSWORD_PATTERN, value) is None:
            raise serializers.ValidationError(
                _('Password can only contain letters, numbers, -, _ and no shorter than 8 and no longer than 20'))
        return value

    @staticmethod
    def validate_email(value):
        if len(value) > 100:
            raise serializers.ValidationError(_('Email address is too long'))
        try:
            User.objects.get(email=value)
            raise serializers.ValidationError(_('Email address occupied'))
        except ObjectDoesNotExist:
            pass
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    captcha = serializers.CharField()

    def validate_captcha(self, value):
        request = self.context['request']
        if not CaptchaAPI.verify_captcha(request, value):
            raise serializers.ValidationError(_('Captcha verify error.'))
        return value

    @staticmethod
    def validate_new_password(value):
        if re.match(PASSWORD_PATTERN, value) is None:
            raise serializers.ValidationError(
                _('Password can only contain letters, numbers, -, _ and no shorter than 8 and no longer than 20'))
        return value

    def validate_old_password(self, old):
        user = self.context['user']
        if not auth.authenticate(username=user.username,
                                 password=old):
            raise serializers.ValidationError(_('Old password error'))
        return old

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError(_('The new password cannot be the same as the old password'))
        return attrs

    def save(self, **kwargs):
        user = self.context['user']
        user.set_password(self.validated_data['new_password'])
        user.save()


class ActivityListSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = Activity
        fields = ['id', 'user', 'info', 'category', 'info', 'create_time']


class RankSerializer(serializers.ModelSerializer):
    student = StudentInfoShortSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'total_passed',
                  'total_accepted',
                  'total_submitted',
                  'student']


class FollowingSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    follow = serializers.BooleanField()

    @staticmethod
    def validate_user_id(value):
        try:
            User.objects.get(id=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(_('User not exist.'))
        return value


class POSTCheckEmailAddressSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    captcha = serializers.CharField()

    def validate_captcha(self, value):
        request = self.context['request']
        if not CaptchaAPI.verify_captcha(request, value):
            raise serializers.ValidationError(_('Captcha verify error.'))
        return value

    @staticmethod
    def validate_email(value):
        try:
            User.objects.get(email=value)
            raise serializers.ValidationError(_('Email address occupied'))
        except ObjectDoesNotExist:
            pass
        return value

    def save(self):
        activate_code = '%06d' % random.randint(0, 999999)
        email = str(self.validated_data['email']).encode('utf-8')
        cache.set(f'check-email-code-{md5(email).hexdigest()}', activate_code, ACTIVATE_CODE_AGE)
        return activate_code


class PUTChangeEmailAddressSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    verify_code = serializers.CharField(max_length=6, min_length=6)

    def validate(self, data):
        email = str(data["email"]).encode('utf-8')
        if cache.get(f'check-email-code-{md5(email).hexdigest()}') != data['verify_code']:
            raise serializers.ValidationError(_('Email verify code error'))
        return data

    def save(self, **kwargs):
        user = self.context['user']
        user.email = self.validated_data['email']
        user.save()
        cache.delete(f'check-email-code-{md5(str(user.email).encode("utf-8")).hexdigest()}')


class StudentInfoSerializer(serializers.ModelSerializer):
    def save(self, user: User):
        try:
            user.student.school = self.validated_data['school']
            user.student.student_id = self.validated_data['student_id']
            user.student.save()
        except StudentInfo.DoesNotExist:
            StudentInfo(user=user, school=self.validated_data['school'],
                        student_id=self.validated_data['student_id']).save()

    class Meta:
        model = StudentInfo
        fields = ('school', 'student_id')