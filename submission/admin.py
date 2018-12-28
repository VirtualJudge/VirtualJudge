from django.contrib import admin
from submission.models import Submission


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'remote_oj', 'remote_id', 'verdict', 'unique_key', 'verdict_info', 'hook', 'status')


admin.site.register(Submission, SubmissionAdmin)
