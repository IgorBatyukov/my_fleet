from django.contrib import admin
from . import models


@admin.register(models.Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_location', 'office_phone_num', 'mobile_phone_num_1', 'email_1']
    empty_value_display = 'not provided'


@admin.register(models.Voyage)
class VoyageAdmin(admin.ModelAdmin):
    list_display = ['voy_num', 'get_vessel', 'type', 'get_departure_port', 'is_completed']


@admin.register(models.Cargo)
class CargoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CargoOps)
class CargoOpsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Bunker)
class BunkerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BunkerOps)
class BunkerOpsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BunkerDailyBalance)
class BunkerDailyBalanceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VesselPosition)
class VesselPositionAdmin(admin.ModelAdmin):
    pass



