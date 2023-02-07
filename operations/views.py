from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import NoonReportForm, ArrivalReportForm, DepartureReportForm, BunkeringReportForm


class ReportView(FormView):
    form_class = NoonReportForm
    template_name = 'operations/report.html'


