from django.contrib import admin
from account.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_admin')
    fieldsets = (('Basic', {'fields': ('username', 'email', 'is_admin')}),)


admin.site.register(UserProfile, UserProfileAdmin)
