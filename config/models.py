from django.db import models


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

    class Meta:
        db_table = 'remote_account'
