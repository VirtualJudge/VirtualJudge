from django.contrib import admin
from django.contrib.auth.models import Permission

from user.models import Activity, User, StudentInfo

# Register your models here.

admin.site.register(Permission)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'info', 'create_time')
    list_filter = ('user',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_superuser', 'date_joined')
    list_filter = ('username',)


class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school')


admin.site.register(Activity, ActivityAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(StudentInfo, StudentInfoAdmin)
