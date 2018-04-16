from django.contrib import admin
from remote.models import Setting
from remote.models import Account, Language


class SettingAdmin(admin.ModelAdmin):
    list_display = ('oj_key', 'oj_value')


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_language', 'oj_language_name')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_username', 'oj_password', 'oj_account_status', 'update_time')
    list_editable = ('oj_account_status')


admin.site.register(Language, LanguageAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Setting, SettingAdmin)
