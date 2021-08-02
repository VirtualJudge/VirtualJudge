from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import Response

from user.models import User, StudentInfo
from user.perm import ManageUserPermission
from user.serializers import UserInfoSerializer, LoginSerializer, RegisterSerializer, \
    ChangePasswordSerializer, ActivityListSerializer, AdvancedUserInfoSerializer, RankSerializer, \
    FollowingSerializer, PUTChangeEmailAddressSerializer, POSTCheckEmailAddressSerializer, StudentInfoSerializer
from utils.response import msg
from utils.tools import random_str
# from user.tasks import send_activated_email
from vj.settings import DEBUG as VJ_DEBUG


# Administrator's operations
class AdvancedUserViewSet(viewsets.GenericViewSet,
                          UpdateModelMixin,
                          ListModelMixin,
                          RetrieveModelMixin):
    serializer_class = AdvancedUserInfoSerializer
    permission_classes = [ManageUserPermission]
    queryset = User.objects.all()

    # Use administrator's privilege to get single guy's information
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(msg(serializer.data))

    # Use administrator's privilege to update someone's information
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(msg(serializer.data))

    # Use administrator's privilege to list user
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(msg(serializer.data))

    # Use administrator's privilege to reset some one's password
    @action(methods=['POST'], detail=True)
    def reset_password(self, request, pk=None, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        new_password = random_str(8)
        user.set_password(new_password)
        user.save()
        return Response(msg({
            'new_password': new_password
        }))


# Simple user operations
class UserViewSet(viewsets.GenericViewSet, ListModelMixin):
    serializer_class = RankSerializer
    queryset = User.objects.all()
    lookup_value_regex = r'\d+'

    # 查询登录状态和登录信息
    @action(methods=['GET'], detail=False)
    def info(self, request):
        if request.user.is_authenticated:
            return Response(msg(self.get_serializer(request.user).data))
        else:
            return Response(msg(err=_('Not login.')))

    # 登录
    @action(methods=['POST'], detail=False)
    def login(self, request):
        if request.user.is_authenticated:
            return Response(msg(err=_('Please sign out first before try to login.')))
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            return Response(msg(UserInfoSerializer(serializer.login(request)).data))
        except Exception as e:
            return Response(msg(err=str(e)))

    # 注册
    @action(methods=['PUT'], detail=False)
    def register(self, request):
        if request.user.is_authenticated:
            return Response(msg(err=_('Please sign out first before try to register.')))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(msg(UserInfoSerializer(user).data))

    # 退出登陆
    @action(methods=['DELETE'], detail=False)
    def logout(self, request):
        auth.logout(request)
        return Response(msg(_('Successful logout.')))

    # 获取个人信息
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        return Response(msg(self.get_serializer(user).data))

    # 修改密码
    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated])
    def password(self, request: Request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user, 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        auth.logout(request)
        return Response(msg(_('Success')))

    # 获取活动记录
    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def activities(self, request: Request, pk=None, *args, **kwargs):
        if request.user.id == pk or request.user.is_staff:
            user = get_object_or_404(User.objects.all(), pk=pk)
            serializer = self.get_serializer(user.activities.all()[:10], many=True)
            return Response(msg(serializer.data))
        raise PermissionDenied

    # User Rank List
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        #        queryset = sorted(queryset, key=lambda x: (-x.total_passed, x.total_submitted, x.id))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(msg(serializer.data))

    # GET: Get user following list
    # POST: Change user following status
    @action(methods=['GET', 'POST'], detail=False, permission_classes=[IsAuthenticated])
    def following(self, request, *args, **kwargs):
        if request.method == 'GET':
            queryset = self.filter_queryset(request.user.following.all())
   #         queryset = sorted(queryset, key=lambda x: (-x.total_passed, x.total_submitted, x.id))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(msg(serializer.data))
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if serializer.validated_data['follow']:
                request.user.following.add(serializer.validated_data['user_id'])
            else:
                request.user.following.remove(serializer.validated_data['user_id'])
            return Response(msg('Success.'))

    # If user(pk) has followed by login user?
    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def followed(self, request, pk=None, *args, **kwargs):
        return Response(msg({
            'followed': int(pk) in list(map(lambda user: user.id, request.user.following.all()))
        }))

    # update self's permission
    # Usage: send POST method first, then server will send an check email to your new address.
    #        then send PUT method to update your email address.
    @action(methods=['POST'], detail=False)
    def check_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        verify_code = serializer.save()
        if VJ_DEBUG:
            print("verify code:", verify_code)
        # send_activated_email.apply_async(args=[serializer.validated_data['email'], verify_code], queue='result')
        return Response(msg(_('please check your new email box to get verify code.')))

    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated])
    def email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(msg(_('Change email address success.')))

    # update and get user student information
    @action(methods=['POST', 'GET'], detail=False, permission_classes=[IsAuthenticated])
    def student(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(request.user)
            return Response(msg(serializer.data))
        else:
            try:
                serializer = self.get_serializer(request.user.student)
            except StudentInfo.DoesNotExist:
                return Response(msg({}))
            return Response(msg(serializer.data))

    def get_serializer_class(self):
        if self.action in ['info', 'retrieve']:
            return UserInfoSerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'register':
            return RegisterSerializer
        elif self.action == 'password':
            return ChangePasswordSerializer
        elif self.action == 'activities':
            return ActivityListSerializer
        elif self.action == 'list':
            return RankSerializer
        elif self.action == 'following':
            if self.request.method == 'GET':
                return RankSerializer
            return FollowingSerializer
        elif self.action == 'email':
            return PUTChangeEmailAddressSerializer
        elif self.action == 'check_email':
            return POSTCheckEmailAddressSerializer
        elif self.action == 'student':
            return StudentInfoSerializer
        return self.serializer_class
