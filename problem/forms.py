from django import forms


class GetProblemByIdForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class GetProblemByRemoteInfoForm(forms.Form):
    remote_oj = forms.CharField(max_length=20)
    remote_id = forms.CharField(max_length=20)
    force_update = forms.BooleanField(required=False)


class GetProblemListForm(forms.Form):
    offset = forms.IntegerField(min_value=1)
    limit = forms.IntegerField(min_value=1, max_value=50)
