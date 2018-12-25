from django.contrib import admin
from support.models import Setting
from support.models import Account, Language, Support


class SupportAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_enable', 'oj_status')


class SettingAdmin(admin.ModelAdmin):
    list_display = ('oj_key', 'oj_value')


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_language', 'oj_language_name')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_username', 'oj_password', 'update_time')


admin.site.register(Language, LanguageAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Support, SupportAdmin)
