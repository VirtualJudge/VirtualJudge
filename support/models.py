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
        db_table = 'languages'
        unique_together = ('oj_name', 'oj_language')


class Account(models.Model):
    oj_name = models.CharField(max_length=20)
    oj_username = models.CharField(max_length=30)
    oj_password = models.CharField(max_length=100)
    update_time = models.DateTimeField(auto_now=True)
    cookies = JSONField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=True)

    class Meta:
        db_table = 'accounts'
        unique_together = ('oj_name', 'oj_username')


class Support(models.Model):
    STATUS_CHOICES = (('PENDING', '等待中'), ('SUCCESS', '成功'), ('FAILED', '失败'))

    oj_name = models.CharField(max_length=20, primary_key=True)
    oj_proxies = models.CharField(max_length=200, default=None, blank=True, null=True)
    oj_enable = models.BooleanField(default=False)
    oj_status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='PENDING')

    class Meta:
        db_table = 'support'
