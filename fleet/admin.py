from django.contrib import admin
from . import models


@admin.register(models.Fleet)
class FleetAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_vessels']


@admin.register(models.Vessel)
class VesselAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_fleet']
