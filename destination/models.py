from django.db import models


# Create your models here.

class Platform(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=100, default="")
    enable = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'platform'


class Language(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT, blank=False, null=False)
    key = models.CharField(max_length=20, null=False, blank=False)
    display = models.CharField(max_length=40)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.platform.name + ':' + self.display

    class Meta:
        db_table = 'language'
        unique_together = ('platform', 'key')
