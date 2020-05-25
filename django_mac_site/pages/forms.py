from django import forms

class InfoForm(forms.Form):
    serial = forms.CharField(label='', max_length=20, widget=forms.TextInput(
    attrs={'id': 'search-field', 'class': 'form-control searchTerm', 'placeholder': 'Enter WSID or Serial #'}))


class DEPForm(forms.Form):
    serial = forms.CharField(label='', max_length=20, widget=forms.TextInput(
    attrs={'id': 'search-field', 'class': 'form-control searchTerm', 'placeholder': 'Enter Serial # to search'}))
