from django import forms


class PostRegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=250)


class PostLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=100)
