from django.contrib import admin
from . import models


@admin.register(models.CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'rank', 'fleet']
    list_editable = ['fleet']
    list_per_page = 10


@admin.register(models.Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.CertificationMatrix)
class CertificationMatrixAdmin(admin.ModelAdmin):
    list_display = ['rank', 'certificate', 'vessel_type']


@admin.register(models.CrewCertification)
class CrewCertificationAdmin(admin.ModelAdmin):
    list_display = ['crew', 'cert', 'valid_to']


@admin.register(models.CrewMedicalExamination)
class CrewMedicalExaminationAdmin(admin.ModelAdmin):
    list_display = ['get_crew', 'get_medical_center', 'valid_to']


@admin.register(models.CrewChange)
class CrewChangeAdmin(admin.ModelAdmin):
    list_display = ['crew',
                    'vessel',
                    'date',
                    'port',
                    'type',
                    'manager']


@admin.register(models.SalaryMatrix)
class SalaryMatrixAdmin(admin.ModelAdmin):
    list_display = ['get_rank', 'basic', 'performance_bonus', 'leave_payment', 'get_total']


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['manager', 'crew', 'duration', 'offset', 'signed_date']
