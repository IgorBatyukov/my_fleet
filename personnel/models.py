from django.db import models
from fleet.models import Fleet
from geo.models import City


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

    name = models.CharField(max_length=15)
    father_name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=25)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    marriage_status = models.CharField(max_length=7, choices=MARRIAGE_STATUS, default=SINGLE)
    position = models.ManyToManyField(Position, through='EmployeePosition', verbose_name='position')
    fleet = models.ManyToManyField(Fleet, through='EmployeePosition', verbose_name='fleet')

    def __str__(self):
        return f'{self.name} {self.father_name} {self.surname}'


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
