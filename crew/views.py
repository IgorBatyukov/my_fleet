from django.db.models import Q, Count
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin

from .forms import CrewChangeForm, ContractForm
from .models import CrewMember, VesselsSchedule, CrewOnBoard, CrewList, CrewChange, Contract
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
        vessel_id = self.kwargs['pk']
        vessel_details = queryset.get(vessel_id=vessel_id)
        return vessel_details

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        vessel_id = self.kwargs['pk']
        context['crew_onboard'] = CrewOnBoard.objects.filter(vsl_id=vessel_id)
        return context


class CrewListView(ListView):
    template_name = 'crew/crew_list.html'
    model = CrewList
    context_object_name = 'crew_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        fleet_id = 1
        crew_list = queryset.filter(fleet_id=fleet_id)
        return crew_list


class CrewDetailsView(ListView):
    template_name = 'crew/crew_details.html'
    model = CrewMember
    context_object_name = 'crew_member'

    def get_queryset(self):
        queryset = super().get_queryset()
        crew_id = self.kwargs['pk']
        crew_member = queryset.get(id=crew_id)
        return crew_member

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['certificates'] = CrewMember.get_certificates(CrewMember.objects.get(id=self.kwargs['pk']))
        return context


class CrewChangeView(ListView):
    template_name = 'crew/crew_change.html'
    model = CrewChange
    context_object_name = 'crew_changes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crew_changes_agg'] = CrewChange.get_crew_changes_list()
        return context


class CrewChangeDetailsView(ListView):
    template_name = 'crew/crew_change_details.html'
    model = CrewChange
    context_object_name = 'crew_change'

    def get_queryset(self):
        queryset = super().get_queryset()
        vessel = self.kwargs['vessel__name']
        date = self.kwargs['date']
        port = self.kwargs['port__name']
        change_type = self.kwargs['type']
        crew_change = queryset.filter(Q(vessel__name=vessel) &
                                      Q(date=date) &
                                      Q(port__name=port) &
                                      Q(type=change_type)
                                      ).order_by('crew__rank')
        return crew_change

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        agency_query = CrewChangeDetailsView.get_queryset(self).values('agency__name').annotate(Count('id'))
        agency = agency_query[0]['agency__name']
        context['change_info'] = {'vessel': self.kwargs['vessel__name'],
                                  'date': self.kwargs['date'],
                                  'port': self.kwargs['port__name'],
                                  'type': self.kwargs['type'],
                                  'agency': agency
                                  }
        return context


class CrewChangeAdd(CreateView):
    template_name = 'crew/crew_change_add.html'
    model = CrewChange
    form_class = CrewChangeForm
    success_url = reverse_lazy('crew_change')


class ContractMainView(ListView):
    template_name = 'crew/contract_list.html'
    model = Contract
    context_object_name = 'contracts'


class ContractAdd(CreateView):
    template_name = 'crew/contract_add.html'
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('contracts_list')

