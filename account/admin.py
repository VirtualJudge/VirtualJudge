from django.contrib import admin
from account.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_admin')
    fieldsets = (['Main', {'fields': ('username', 'email', 'password'), }],
                 ['Advance', {'fields': ('is_active', 'is_admin'), }])


admin.site.register(UserProfile, UserProfileAdmin)
