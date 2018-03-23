from django.contrib import admin
from problem.models import Problem


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('remote_oj', 'remote_id', 'request_status', 'update_time')


admin.site.register(Problem, ProblemAdmin)
