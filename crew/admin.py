from django.contrib import admin
from . import models


@admin.register(models.CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'get_rank', 'working_status', 'get_vessel']


@admin.register(models.Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.CertificationMatrix)
class CertificationMatrixAdmin(admin.ModelAdmin):
    list_display = ['get_rank', 'get_certificate']


@admin.register(models.CrewCertification)
class CrewCertificationAdmin(admin.ModelAdmin):
    list_display = ['get_crew', 'get_certificate', 'valid_to']


@admin.register(models.CrewMedicalExamination)
class CrewMedicalExaminationAdmin(admin.ModelAdmin):
    list_display = ['get_crew', 'get_medical_center', 'valid_to']


@admin.register(models.EducationCenter)
class EducationCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_location']


@admin.register(models.MedicalCenter)
class MedicalCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_location']


@admin.register(models.CrewOnVessel)
class CrewOnVesselAdmin(admin.ModelAdmin):
    list_display = ['get_crew', 'get_vessel', 'signed_on', 'signed_off']


@admin.register(models.CrewPosition)
class CrewPositionAdmin(admin.ModelAdmin):
    list_display = ['get_crew', 'get_rank', 'hired_from', 'hired_to']


@admin.register(models.SalaryMatrix)
class SalaryMatrixAdmin(admin.ModelAdmin):
    list_display = ['get_rank', 'basic', 'performance_bonus', 'leave_payment', 'get_total']


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['manager', 'get_crew', 'duration', 'offset', 'signed_date']
