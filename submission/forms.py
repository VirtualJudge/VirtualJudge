from django import forms


class SubmissionForm(forms.Form):
    problem_id = forms.IntegerField(min_value=1)
    code = forms.CharField()
    language = forms.CharField(max_length=20)
