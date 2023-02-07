from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import CrewMember


class CrewingMainView(ListView):
    template_name = 'crew/crew_list.html'
    model = CrewMember
    context_object_name = 'crew'


class VesselsMainView(ListView):
    pass


class VesselDetailsView(DetailView):
    pass


class CrewMainView(ListView):
    pass


class CrewDetailsView(DetailView):
    template_name = 'crew/crew_details.html'
    model = CrewMember


