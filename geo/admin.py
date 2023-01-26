from django.contrib import admin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code']


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_country']
