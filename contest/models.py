from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.


class Contest(models.Model):
    title = models.CharField(max_length=50)
    user = models.CharField(max_length=20)
    start_time = models.DateTimeField(auto_now=True)
    problems = ArrayField(models.IntegerField(), blank=True, null=True,
                          max_length=30)

    end_time = models.DateTimeField(auto_now=True)

    created_time = models.DateTimeField(auto_now_add=True)

    password = models.CharField(max_length=20, null=True)

    class Meta:
        ordering = ('created_time',)
        db_table = 'contest'


class ContestProblem(models.Model):
    remote_oj = models.CharField(max_length=20)
    remote_id = models.CharField(max_length=20)
    alias = models.CharField(max_length=10, null=True)
    contest_id = models.IntegerField()

    class Meta:
        ordering = ('contest_id',)
        db_table = 'contest_problem'
