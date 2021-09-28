from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100, widget=forms.TextInput(attrs={'id': 'test1'}))


class ServiceForm(forms.Form):
    docheckbox1 = forms.CharField(max_length=2, required=False, widget=forms.TextInput(attrs={'id': 'docheckbox1', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 1}))
    docheckbox2 = forms.CharField(max_length=2, required=False, widget=forms.TextInput(attrs={'id': 'docheckbox2', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 2}))
    docheckbox3 = forms.CharField(max_length=2, required=False, widget=forms.TextInput(attrs={'id': 'docheckbox3', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 3}))
    docheckbox4 = forms.CharField(max_length=2, required=False, widget=forms.TextInput(attrs={'id': 'docheckbox4', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 4}))
    docheckbox5 = forms.CharField(max_length=2, required=False, widget=forms.TextInput(attrs={'id': 'docheckbox5', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 5}))
    docheckbox6 = forms.CharField(max_length=2, required=False, widget=forms.TextInput(attrs={'id': 'docheckbox6', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 6}))
    docheckbox7 = forms.CharField(max_length=2, required=False, widget=forms.TextInput(attrs={'id': 'docheckbox7', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 7}))
    docheckbox8 = forms.CharField(max_length=2, required=False, widget=forms.TextInput(attrs={'id': 'docheckbox8', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 8}))
    docheckbox9 = forms.CharField(max_length=2, required=False, widget=forms.TextInput(attrs={'id': 'docheckbox9', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 9}))



  
# creating a form 
class GeeksForm(forms.Form):
    GEEKS_CHOICES =(
        ("1", "One"),
        ("2", "Two"),
        ("3", "Three"),
        ("4", "Four"),
        ("5", "Five"),
    )
    geeks_field = forms.ChoiceField(choices = GEEKS_CHOICES, widget=forms.Select(attrs={'class': 'form-control mb-2'}))