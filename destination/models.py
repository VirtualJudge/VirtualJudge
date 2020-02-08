from django.db import models


# Create your models here.

class Platform(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=100, default="")
    enable = models.BooleanField(default=False)

    class Meta:
        db_table = 'platform'
