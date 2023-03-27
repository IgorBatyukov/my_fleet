from django import forms
from .models import CrewChange, Contract


class CrewChangeForm(forms.ModelForm):

    class Meta:
        model = CrewChange
        fields = ['crew', 'vessel', 'date', 'port', 'type', 'agency', 'manager']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ['manager', 'crew', 'duration', 'offset', 'signed_date', 'finished_date', 'vessel', 'rank']

        widgets = {
            'signed_date': forms.DateInput(attrs={'type': 'date'}),
        }
