from django.contrib import admin
from contest.models import Contest


# Register your models here.


class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time')


admin.site.register(Contest, ContestAdmin)
