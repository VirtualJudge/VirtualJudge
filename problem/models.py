from django.db import models

from submission.config import Verdict




# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.JSONField()
    time_limit = models.IntegerField(default=0, null=False, blank=False)
    memory_limit = models.IntegerField(default=0, null=False, blank=False)
    last_update = models.DateTimeField(auto_now=True, editable=False)
    remote_oj = models.CharField(max_length=20, null=False, blank=False)
    remote_id = models.CharField(max_length=20, null=False, blank=False)
    remote_url = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f'{self.id}-{self.title}'

    @property
    def total_accepted(self):
        return self.submissions.filter(verdict=Verdict.ACCEPTED).count()

    @property
    def total_submitted(self):
        return self.submissions.count()

    class Meta:
        ordering = ['id']
