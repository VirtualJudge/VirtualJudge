from django.db import models
from user.models import Profile
from destination.models import Language
from problem.models import Problem
import hashlib


# Create your models here.

class Submission(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    submit_time = models.DateTimeField(auto_now_add=True)

    code = models.TextField(null=True, blank=True)
    code_md5 = models.CharField(null=True, blank=True, max_length=100)

    result = models.CharField(max_length=100, default='')
    extra_msg = models.TextField()
    update_time = models.DateTimeField(auto_now=True)

    def save(self, request=None, *args, **kwargs):
        self.user = request.user
        self.code_md5 = hashlib.md5(self.code.strip().encode(encoding='UTF-8')).hexdigest()
        super().save(*args, **kwargs)
