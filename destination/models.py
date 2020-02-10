from django.db import models


# Create your models here.

class Platform(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=100, default="")
    enable = models.BooleanField(default=False)

    class Meta:
        db_table = 'platform'


class Language(models.Model):
    platform = models.CharField(max_length=20)
    key = models.CharField(max_length=20, null=False, blank=False)
    display = models.CharField(max_length=40)
    enable = models.BooleanField(default=True)

    class Meta:
        db_table = 'language'
