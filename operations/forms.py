from django import forms
from operations.models import VesselPositionReport


class NoonReportForm(forms.ModelForm):
    class Meta:
        model = VesselPositionReport
        fields = '__all__'


class ArrivalReportForm(forms.ModelForm):
    pass


class DepartureReportForm(forms.ModelForm):
    pass


class BunkeringReportForm(forms.ModelForm):
    pass

