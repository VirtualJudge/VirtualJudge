from django.db import models

from problem.models import Problem
from submission.config import Verdict
from user.models import User
from contest.models import Contest


# Create your models here.

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='submissions', null=True)

    code = models.TextField()
    verdict = models.CharField(max_length=10, default=Verdict.PENDING, choices=Verdict.VERDICT_CHOICES)
    remote_verdict = models.CharField(max_length=100, default="", null=True, blank=True)
    lang = models.CharField(max_length=20, null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True)
    time_cost = models.CharField(max_length=10, null=True, blank=True)
    memory_cost = models.CharField(max_length=10, null=True, blank=True)
    # 程序编译运行的时候返回的一些错误信息和编译失败的错误信息
    additional_info = models.JSONField(default=None, null=True)

    is_public = models.BooleanField(default=False)

    # hash
    hash_val = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'<Submission>id:{self.id} problem: {self.problem.id} verdict: {self.verdict}'

    class Meta:
        ordering = ['-id']
