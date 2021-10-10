from django import forms

# class NameForm(forms.Form):
#     name = forms.CharField(label='Your name', max_length=100, widget=forms.TextInput(attrs={'id': 'test1'}))

# class Checkbox(forms.Form):
#     test1 = forms.BooleanField( widget=forms.TextInput(attrs={'id': 'docheckbox1', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 1}))


class ServiceForm(forms.Form):
    docheckbox1 = forms.BooleanField(required=False, widget=forms.TextInput(attrs={'id': 'docheckbox1', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 1}))
    docheckbox2 = forms.BooleanField(required=False, widget=forms.TextInput(attrs={'id': 'docheckbox2', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 2}))
    docheckbox3 = forms.BooleanField(required=False, widget=forms.TextInput(attrs={'id': 'docheckbox3', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 3}))
    docheckbox4 = forms.BooleanField(required=False, widget=forms.TextInput(attrs={'id': 'docheckbox4', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 4}))
    docheckbox5 = forms.BooleanField(required=False, widget=forms.TextInput(attrs={'id': 'docheckbox5', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 5}))
    docheckbox6 = forms.BooleanField(required=False, widget=forms.TextInput(attrs={'id': 'docheckbox6', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 6}))
    docheckbox7 = forms.BooleanField(required=False, widget=forms.TextInput(attrs={'id': 'docheckbox7', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 7}))
    docheckbox8 = forms.BooleanField(required=False, widget=forms.TextInput(attrs={'id': 'docheckbox8', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 8}))
    docheckbox9 = forms.BooleanField(required=False, widget=forms.TextInput(attrs={'id': 'docheckbox9', 'type': 'checkbox', 'class': 'form-check-input position-static', 'value': 9}))


class BranchForm(forms.Form):
    GEEKS_CHOICES =(
        ("1", "เชลล์พลูตาหลวง (ตรงข้ามโรงพยาบาล กม.10)"),
        ("2", "เชลล์อู่ตะเภา (หน้าโรงเรียนพลูตาหลวง)")
    )
    branch = forms.ChoiceField(required=False, choices = GEEKS_CHOICES, widget=forms.Select(attrs={'class': 'form-control mb-2"'}))
    


class WebForm(ServiceForm):

    # full_name = forms.BooleanField( widget=forms.TextInput(attrs={'id': 'full_name', 'name': "fullname", 'class': 'form-check-input position-static', 'value': 1, 
    #     'onfocusout': 'validateNull()', 'value': '{{ user.full_name|default:""}}', 'class': 'form-control form-input'
    # }))
    # date = 
    def test(self):
        return
    # first_name = forms.CharField(widget=forms.Select(attrs={'class': 'form-control form-input'}))
    # first_name = forms.CharField(widget=forms.Select(attrs={'class': 'form-control form-input'}))

