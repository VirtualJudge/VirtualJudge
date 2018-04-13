from django.contrib.postgres.fields import ArrayField
from django.core.validators import ValidationError
from django.db import models
from django.utils import timezone


# Create your models here.

def start_time_validate(value):
    if value <= timezone.now():
        raise ValidationError('start_time should after now')


def time_delta_validate(value):
    if value < timezone.timedelta(minutes=1):
        raise ValidationError('process_time too short, min = 1 min')
    if value > timezone.timedelta(hours=8640):
        raise ValidationError('process_time too long,max = 360 day')


class Contest(models.Model):
    title = models.CharField(max_length=50)
    user = models.CharField(max_length=20)
    problems = ArrayField(models.IntegerField(), blank=True, null=True, max_length=30)
    start_time = models.DateTimeField(validators=[start_time_validate])
    time_delta = models.DateTimeField(default=timezone.timedelta(hours=5), validators=[time_delta_validate])

    created_time = models.DateTimeField(auto_created=True)

    group = models.IntegerField(null=True)
    password = models.CharField(max_length=20, null=True)

    class Meta:
        ordering = ('created_time',)
        db_table = 'contest'
