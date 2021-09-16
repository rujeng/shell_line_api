from django import forms

class WebForm(forms.Form):
    fullname = forms.CharField(max_length=20)