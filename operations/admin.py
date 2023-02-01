from django.contrib import admin
from . import models


@admin.register(models.Agency)
class AgencyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Voyage)
class VoyageAdmin(admin.ModelAdmin):
    pass


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



