from django.contrib import admin
from . import models


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'phone', 'email']


@admin.register(models.EmployeePosition)
class EmployeePosition(admin.ModelAdmin):
    list_display = ['get_employee', 'get_position', 'get_fleet']
