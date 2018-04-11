from django.db import models


class SettingOJ(models.Model):
    oj_key = models.CharField(max_length=100, primary_key=True)
    oj_value = models.TextField()

    class Meta:
        db_table = 'setting'


class RemoteOJ(models.Model):
    oj_name = models.CharField(max_length=20, primary_key=True)
    oj_status = models.BooleanField(default=True)

    class Meta:
        db_table = 'remote_oj'


class RemoteLanguage(models.Model):
    oj_name = models.CharField(max_length=20, null=True)
    oj_language = models.CharField(max_length=10, null=True)
    oj_language_name = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'remote_language'


class RemoteAccount(models.Model):
    oj_name = models.CharField(max_length=20, null=True)
    oj_username = models.CharField(max_length=20, null=True)
    oj_password = models.CharField(max_length=100, null=True)
    oj_account_status = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'remote_account'
