from django import forms


class RemoteAccountForm(forms.Form):
    remote_account = forms.CharField()
