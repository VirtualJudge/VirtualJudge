from django import forms


class RemoteAccountForm(forms.Form):
    remote_accounts = forms.FileField()
