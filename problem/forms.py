from django import forms


class GetProblemByIdForm(forms.Form):
    id = forms.IntegerField(min_value=1)


class GetProblemByRemoteInfoForm(forms.Form):
    remote_oj = forms.CharField(max_length=20)
    remote_id = forms.CharField(max_length=20)
    force_update = forms.BooleanField(required=False)


class GetProblemListForm(forms.Form):
    page_number = forms.IntegerField(min_value=1)
    page_size = forms.IntegerField(min_value=10, max_value=50)
