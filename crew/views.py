from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView, TemplateView, UpdateView, CreateView

from fleet.models import Vessel
from .forms import CrewChangeForm, ContractForm, CrewMemberEditForm, CrewCertificateEditForm, CrewCertificateAddForm, \
    CrewChangeOnVesselForm, CrewCertificateAddSpecificForm
from .models import CrewMember, CrewOnBoard, CrewList, CrewChange, Contract, CrewCertification, \
    CertificationMatrix
from operations.models import VesselsSchedule


class CrewingMainView(LoginRequiredMixin, TemplateView):
    template_name = 'crew/home.html'


class VesselsMainView(LoginRequiredMixin, ListView):
    template_name = 'crew/vessels.html'
    model = VesselsSchedule
    context_object_name = 'vessels'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        fleet_list = user.employee.get_fleet_list()
        fleet_vessels = queryset.filter(fleet__in=fleet_list)
        return fleet_vessels


class VesselDetailsView(LoginRequiredMixin, ListView):
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


class CrewListView(LoginRequiredMixin, ListView):
    template_name = 'crew/crew_list.html'
    model = CrewList
    context_object_name = 'crew_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        fleet_list = user.employee.get_fleet_list()
        crew_list = queryset.filter(fleet_name__in=fleet_list)
        return crew_list


class CrewDetailsView(LoginRequiredMixin, ListView):
    template_name = 'crew/crew_details.html'
    model = CrewMember
    context_object_name = 'crew_member'

    def get_queryset(self):
        queryset = super().get_queryset()
        crew_id = self.kwargs['pk']
        crew_member = queryset.get(id=crew_id)
        return crew_member


class CrewCertificationMatrixView(LoginRequiredMixin, ListView):
    template_name = 'crew/crew_certification_matrix.html'
    model = CertificationMatrix
    context_object_name = 'matrix'

    def get_queryset(self):
        queryset = super().get_queryset()
        crew_rank = self.kwargs['rank_id']
        cert_matrix = queryset.filter(rank=crew_rank)
        return cert_matrix

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vessel_types'] = CertificationMatrix.get_vessel_type_list()
        context['certificates_for_sailor'] = CrewCertification.get_certificates_for_sailor(self.kwargs['pk'])
        context['sailor'] = CrewMember.objects.get(id=self.kwargs['pk'])
        return context


class CrewChangeView(LoginRequiredMixin, ListView):
    template_name = 'crew/crew_change.html'
    model = CrewChange
    context_object_name = 'crew_changes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crew_changes_agg'] = CrewChange.get_crew_changes_list()
        return context


class CrewChangeDetailsView(LoginRequiredMixin, ListView):
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


class CrewChangeAdd(LoginRequiredMixin, CreateView):
    template_name = 'crew/edit.html'
    model = CrewChange
    form_class = CrewChangeForm
    success_url = reverse_lazy('crew_change')


class CrewChangeAddOnVessel(LoginRequiredMixin, CreateView):
    template_name = 'crew/edit.html'
    model = CrewChange
    form_class = CrewChangeOnVesselForm

    def get_success_url(self):
        return reverse('vessel_details', kwargs={'pk': self.kwargs['vessel_id']})

    def get_initial(self):
        initial = super().get_initial()
        vessel_id = self.kwargs['vessel_id']
        initial['vessel'] = Vessel.objects.get(id=vessel_id)
        return initial


class ContractMainView(LoginRequiredMixin, ListView):
    template_name = 'crew/contract_list.html'
    model = Contract
    context_object_name = 'contracts'


class ContractAdd(LoginRequiredMixin, CreateView):
    template_name = 'crew/edit.html'
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('contracts_list')


class ContractEdit(LoginRequiredMixin, UpdateView):
    template_name = 'crew/edit.html'
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('contracts_list')


class CrewDetailsEditView(LoginRequiredMixin, UpdateView):
    template_name = 'crew/edit.html'
    model = CrewMember
    form_class = CrewMemberEditForm

    def get_success_url(self):
        return reverse('crew_member_details', kwargs={'pk': self.kwargs['pk']})


class CrewCertificateEdit(LoginRequiredMixin, UpdateView):
    template_name = 'crew/edit.html'
    model = CrewCertification
    form_class = CrewCertificateEditForm

    def get_success_url(self):
        return reverse('crew_member_details', kwargs={'pk': self.kwargs['crew_id']})


class CrewCertificateDelete(LoginRequiredMixin, DeleteView):
    model = CrewCertification

    def get_success_url(self):
        return reverse('crew_member_details', kwargs={'pk': self.kwargs['crew_id']})


class CrewCertificateAdd(LoginRequiredMixin, CreateView):
    template_name = 'crew/edit.html'
    model = CrewCertification
    form_class = CrewCertificateAddForm

    def get_success_url(self):
        return reverse('crew_member_details', kwargs={'pk': self.kwargs['crew_id']})

    def form_valid(self, form):
        certificate = form.save(commit=False)
        certificate.crew_id = self.kwargs['crew_id']
        certificate.save()
        return HttpResponseRedirect(self.get_success_url())


class CrewCertificateAddSpecificView(LoginRequiredMixin, CreateView):
    template_name = 'crew/edit.html'
    model = CrewCertification
    form_class = CrewCertificateAddSpecificForm

    def get_success_url(self):
        next_url = self.request.POST.get('next', '/')
        return next_url

    def form_valid(self, form):
        certificate = form.save(commit=False)
        certificate.crew_id = self.kwargs['crew_id']
        certificate.cert_id = self.kwargs['cert_id']
        certificate.save()
        return HttpResponseRedirect(self.get_success_url())
