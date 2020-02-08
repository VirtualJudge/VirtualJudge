from django.contrib import admin
from user.models import Profile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_admin', 'submitted', 'accepted')
    fieldsets = (('Basic', {'fields': ('username', 'nickname', 'email', 'submitted', 'accepted')}),)


admin.site.register(Profile, UserProfileAdmin)
