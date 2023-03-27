from django.db import models
from fleet.models import Fleet
from geo.models import City
from django.contrib.auth.models import User


class Position(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Employee(models.Model):

    MARRIED = 'married'
    SINGLE = 'single'

    MARRIAGE_STATUS = [
        (MARRIED, 'Married'),
        (SINGLE, 'Single'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)
    location = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    marital_status = models.CharField(max_length=7, choices=MARRIAGE_STATUS, default=SINGLE)
    position = models.ManyToManyField(Position, through='EmployeePosition', verbose_name='position')
    fleet = models.ManyToManyField(Fleet, through='EmployeePosition', verbose_name='fleet')


class EmployeePosition(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE)
    hired_from = models.DateField()
    hired_to = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'hired_from'], name='unique_employee_position')
        ]

    def get_employee(self):
        return self.employee

    def get_position(self):
        return self.position

    def get_fleet(self):
        return self.fleet
