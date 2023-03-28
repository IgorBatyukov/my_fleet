from django import forms
from .models import CrewChange, Contract, CrewMember, CrewCertification


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
            'finished_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CrewMemberEditForm(forms.ModelForm):
    class Meta:
        model = CrewMember
        fields = [
            'name',
            'father_name',
            'surname',
            'birth_date',
            'phone',
            'email',
            'location',
            'marriage_status',
            'rank'
        ]


class CrewCertificateEditForm(forms.ModelForm):

    class Meta:
        model = CrewCertification
        fields = ['cert_number', 'valid_from', 'valid_to']

        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'valid_to': forms.DateInput(attrs={'type': 'date'}),
        }


class CrewCertificateAddForm(forms.ModelForm):

    class Meta:
        model = CrewCertification
        fields = ['cert', 'cert_number', 'valid_from', 'valid_to']

        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'valid_to': forms.DateInput(attrs={'type': 'date'}),
        }
