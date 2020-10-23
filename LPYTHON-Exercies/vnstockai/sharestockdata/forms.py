from django import forms
from .models import StockOrder, StockDayData


class DataForm(forms.Form):
    daydata = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'date'
    }))
    changelimit = forms.FloatField()
