from django.contrib import admin
from remote.models import OJ, Account, Language


class OJAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_status')


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_language', 'oj_language_name')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('oj_name', 'oj_username', 'oj_password', 'oj_account_status', 'update_time')


admin.site.register(Language, LanguageAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(OJ, OJAdmin)
