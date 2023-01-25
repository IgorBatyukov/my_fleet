from django.contrib import admin
from . import models


@admin.register(models.CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'surname', 'get_rank', 'working_status']


@admin.register(models.Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.CertificationMatrix)
class CertificationMatrixAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EducationCenter)
class EducationCenterAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MedicalCenter)
class MedicalCenterAdmin(admin.ModelAdmin):
    pass

