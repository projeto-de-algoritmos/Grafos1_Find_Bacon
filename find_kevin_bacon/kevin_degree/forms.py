from django import forms

class SearchGraphForm(forms.Form):
    search = forms.CharField(label='Busca', max_length=100)