from django import forms


class AddForm(forms.Form):
    hour = forms.IntegerField()
    minute = forms.IntegerField()
    second = forms.IntegerField()
