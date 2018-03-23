from django.contrib import admin
from config.models import RemoteOJ, RemoteAccount, RemoteLanguage


class RemoteOJAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_status')


class RemoteLanguageAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_language', 'oj_language_name')


class RemoteAccountAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_username', 'oj_password', 'oj_account_status')


admin.site.register(RemoteLanguage, RemoteLanguageAdmin)
admin.site.register(RemoteAccount, RemoteAccountAdmin)
admin.site.register(RemoteOJ, RemoteOJAdmin)
