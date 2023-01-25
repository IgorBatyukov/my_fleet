from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from .models import CrewMember


class Login(TemplateView):
    template_name = 'login.html'


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


