from django.contrib.auth.models import AbstractBaseUser
from django.db import models
import uuid


def get_token():
    return str(uuid.uuid4()).replace('-', '')


class Token(models.Model):
    token = models.CharField(max_length=100, primary_key=True, default=get_token())
    nickname = models.CharField(max_length=40, null=True, blank=True)
    privilege = models.IntegerField(default=0)

    class Meta:
        db_table = 'Token'


"""
@:param privilege 0 普通用户 1 高级用户 2 管理员
"""
