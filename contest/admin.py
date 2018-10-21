from django.contrib import admin
from contest.models import Contest, ContestProblem


# Register your models here.


class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


class ContestProblemAdmin(admin.ModelAdmin):
    list_display = ('contest_id', 'remote_oj', 'remote_id', 'alias')


admin.site.register(Contest, ContestAdmin)
admin.site.register(ContestProblem, ContestProblemAdmin)
