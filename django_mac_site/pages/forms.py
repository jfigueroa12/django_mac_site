from django import forms

class InfoForm(forms.Form):
    serial = forms.CharField(label='', max_length=20, widget=forms.TextInput(
    attrs={'class': 'form-control', 'placeholder': 'Enter WSID or serial #'}))
