from django.db import models
from fleet.models import Vessel
from geo.models import SeaPort


class Agency(models):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    office_phone_num = models.CharField(max_length=25)
    mobile_phone_num_1 = models.CharField(max_length=25)
    mobile_phone_num_2 = models.CharField(max_length=25)
    email_1 = models.EmailField()
    email_2 = models.EmailField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'location'], name='unique_agency')
        ]


class Voyage(models.Model):
    voy_num = models.CharField(max_length=15)
    departure = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    destination = models.ManyToManyField(SeaPort)
    is_completed = models.BooleanField(default=False)
    agency = models.ManyToManyField(Agency)


class Cargo(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class NoonReport(models.Model):

    OPERATION = [
        ('sea', 'Vessel is at sea'),
        ('port', 'Vessel is in port'),
        ('drifting', 'Vessel is drifting'),
        ('anchorage', 'Vessel is at anchorage'),
    ]

    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    voy_num = models.CharField(max_length=15)
    report_date = models.DateField()
    utc_offset = models.FloatField()
    current_position = models.CharField(max_length=25)
    operation = models.CharField(max_length=15, choices=OPERATION, default='sea')
    destination = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    eta = models.DateTimeField()
    distance_daily = models.PositiveIntegerField()
    speed_avg = models.PositiveIntegerField()
    course_avg = models.PositiveIntegerField()
    sea_bft = models.PositiveIntegerField()
    swell_bft = models.PositiveIntegerField()
    swell_dir = models.PositiveIntegerField()
    wind_bft = models.PositiveIntegerField()
    wind_dir = models.PositiveIntegerField()
    bunker_vlsfo = models.FloatField()
    bunker_do = models.FloatField()

    def __str__(self):
        return f'Noon position: {self.vessel} - {self.voy_num} - {self.report_date}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['voy_num', 'report_date'], name='unique_noon_report')
        ]


class DepartureReport(models.Model):

    CONDITION = [
        ('ballast', 'Vessel is in ballast condition'),
        ('loaded', 'Vessel is in loaded condition'),
    ]

    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    voy_num = models.CharField(max_length=15)
    report_date_time = models.DateTimeField()
    utc_offset = models.FloatField()
    destination = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    bunker_vlsfo = models.FloatField()
    bunker_do = models.FloatField()
    condition = models.CharField(max_length=10, choices=CONDITION, default='ballast')
    agency = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Departure: {self.vessel} - {self.voy_num} - {self.report_date_time}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['voy_num', 'report_date_time'], name='unique_departure_report')
        ]


class ArrivalReport(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    voy_num = models.CharField(max_length=15)
    report_date_time = models.DateTimeField()
    utc_offset = models.FloatField()
    arrival_port = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    distance_daily = models.PositiveIntegerField()
    bunker_vlsfo = models.FloatField()
    bunker_do = models.FloatField()

    def __str__(self):
        return f'Arrival: {self.vessel} - {self.voy_num} - {self.report_date_time}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['voy_num', 'report_date_time'], name='unique_arrival_report')
        ]


class CargoOnBoard(models.Model):
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    voy_num = models.CharField(max_length=15)
    report_date_time = models.DateTimeField()
    cargo = models.ManyToManyField(Cargo)


class BunkeringReport(models.Model):
    bunkering_date_time = models.DateTimeField()
    location = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    vlsfo_qty = models.FloatField()
    do_qty = models.FloatField()
    supplier = models.CharField(max_length=100)


