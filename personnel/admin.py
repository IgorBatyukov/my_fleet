from django.contrib import admin
from . import models


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ['get_employee', 'get_position', 'get_fleet']
