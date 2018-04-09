from django.db import models
from django.contrib.postgres.fields import JSONField
import json


class Problem(models.Model):
    remote_oj = models.CharField(max_length=20, null=True)
    remote_id = models.CharField(max_length=20, null=True)
    remote_url = models.CharField(max_length=200, null=True)
    request_status = models.IntegerField(default=0)
    retry_count = models.IntegerField(default=0)

    special_judge = models.BooleanField(default=False)
    update_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128, null=True)
    time_limit = models.CharField(max_length=20, null=True)
    memory_limit = models.CharField(max_length=20, null=True)

    html = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('id',)
        db_table = 'problem'


class ProblemBuilder(object):
    @staticmethod
    def build_problem(problem_data):
        ret = Problem()
        if problem_data.get('remote_id'):
            ret.remote_id = problem_data['remote_id']
        if problem_data.get('remote_oj'):
            ret.remote_oj = problem_data['remote_oj']
        if problem_data.get('remote_url'):
            ret.remote_url = problem_data['remote_url']
        if problem_data.get('title'):
            ret.title = problem_data['title']
        if problem_data.get('time_limit'):
            ret.time_limit = problem_data['time_limit']
        if problem_data.get('memory_limit'):
            ret.memory_limit = problem_data['memory_limit']
        if problem_data.get('html'):
            ret.html = problem_data['html']
        return ret

    @staticmethod
    def update_problem(ret, problem_data):
        if problem_data.get('remote_id'):
            ret.remote_id = problem_data['remote_id']
        if problem_data.get('remote_oj'):
            ret.remote_oj = problem_data['remote_oj']
        if problem_data.get('remote_url'):
            ret.remote_url = problem_data['remote_url']
        if problem_data.get('title'):
            ret.title = problem_data['title']
        if problem_data.get('time_limit'):
            ret.time_limit = problem_data['time_limit']
        if problem_data.get('memory_limit'):
            ret.memory_limit = problem_data['memory_limit']
        if problem_data.get('html'):
            ret.html = problem_data['html']
        return ret
