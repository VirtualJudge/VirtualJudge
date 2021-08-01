from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the "celery" program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vj.settings")

app = Celery("oj")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")

# load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.autodiscover_tasks()
