from django.contrib import admin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code']


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_country']


@admin.register(models.Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_city', 'iata_code']


@admin.register(models.SeaPort)
class SeaportAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_country']


@admin.register(models.EducationCenter)
class EducationCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_location']


@admin.register(models.MedicalCenter)
class MedicalCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_location']


@admin.register(models.Shipyard)
class ShipyardAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_city', 'get_country']


