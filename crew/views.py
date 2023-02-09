from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import CrewMember, VesselsSchedule
from fleet.models import Vessel


class CrewingMainView(TemplateView):
    template_name = 'crew/home.html'


class VesselsMainView(ListView):
    template_name = 'crew/vessels.html'
    model = VesselsSchedule
    context_object_name = 'vessels'

    def get_queryset(self):
        queryset = super().get_queryset()
        fleet_vessels = queryset.filter(fleet='A')
        return fleet_vessels


class VesselDetailsView(ListView):
    template_name = 'crew/vessel_details.html'
    model = VesselsSchedule
    context_object_name = 'vessel'

    def get_queryset(self):
        queryset = super().get_queryset()
        id = self.kwargs['pk']
        vessel_details = queryset.get(vessel_id=id)
        return vessel_details


class CrewMainView(ListView):
    pass


class CrewDetailsView(DetailView):
    template_name = 'crew/crew_details.html'
    model = CrewMember


