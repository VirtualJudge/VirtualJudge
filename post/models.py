from django.db import models

from user.models import User


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    last_update = models.DateTimeField(auto_now=True, editable=False)
    content = models.TextField()
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False)

    pin = models.BooleanField(default=False)
    public = models.BooleanField(default=True)
