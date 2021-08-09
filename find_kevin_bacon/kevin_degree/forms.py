from django import forms

class SearchGraphForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Busca', max_length=100)