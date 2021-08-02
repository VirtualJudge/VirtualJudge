from django.db import models
from contest.config import AuthType


# Create your models here.

class Contest(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()
    auth_type = models.CharField(choices=AuthType.TYPE_CHOICES, max_length=20)
