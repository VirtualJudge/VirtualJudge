from django.db import models
from django.contrib.postgres.fields import JSONField


class Setting(models.Model):
    oj_key = models.CharField(max_length=100, primary_key=True)
    oj_value = models.TextField()
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'setting'


class Language(models.Model):
    oj_name = models.CharField(max_length=20)
    oj_language = models.CharField(max_length=40)
    oj_language_name = models.CharField(max_length=40)

    class Meta:
        db_table = 'remote_language'
        unique_together = ('oj_name', 'oj_language')


class Account(models.Model):
    oj_name = models.CharField(max_length=20)
    oj_username = models.CharField(max_length=30)
    oj_password = models.CharField(max_length=100)
    oj_account_status = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now=True)
    cookies = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'remote_account'
        unique_together = ('oj_name', 'oj_username')


class Proxy(models.Model):
    oj_name = models.CharField(max_length=20, primary_key=True)
    oj_proxy = models.CharField(max_length=200)
    oj_proxy_type = models.CharField(default='socks', max_length=10)

    class Meta:
        db_table = 'remote_proxy'
