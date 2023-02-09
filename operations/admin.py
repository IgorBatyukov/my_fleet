from django.contrib import admin
from . import models


@admin.register(models.Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_location', 'office_phone_num', 'mobile_phone_num_1', 'email_1']
    empty_value_display = 'not provided'


@admin.register(models.Voyage)
class VoyageAdmin(admin.ModelAdmin):
    list_display = ['voyage_num', 'get_vessel']


@admin.register(models.DeparturePort)
class DeparturePortAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DestinationPort)
class DestinationPortAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CargoType)
class CargoTypesAdmin(admin.ModelAdmin):
    list_display = ['name', 'imo_class']


@admin.register(models.CargoOps)
class CargoOpsAdmin(admin.ModelAdmin):
    list_display = ['get_voyage', 'ops_date_time', 'cargo', 'operation']


@admin.register(models.BunkerType)
class BunkerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BunkerOps)
class BunkerOpsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BunkerReport)
class BunkerReportAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VesselPositionReport)
class VesselPositionReportAdmin(admin.ModelAdmin):
    pass



