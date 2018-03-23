from django.contrib import admin
from account.models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'privilege', 'token')


admin.site.register(Token, TokenAdmin)
