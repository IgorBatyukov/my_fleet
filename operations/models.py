from django.db import models
from django.contrib import admin
from fleet.models import Vessel
from geo.models import SeaPort


class Agency(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    office_phone_num = models.CharField(max_length=25)
    mobile_phone_num_1 = models.CharField(max_length=25, verbose_name='mobile phone num')
    mobile_phone_num_2 = models.CharField(max_length=25)
    email_1 = models.EmailField(verbose_name='main e-mail')
    email_2 = models.EmailField()

    def __str__(self):
        return f'{self.name}, {self.location}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'location'], name='unique_agency')
        ]
        verbose_name_plural = 'agencies'

    @admin.display(description='location')
    def get_location(self):
        return self.location


class Voyage(models.Model):
    BALLAST = 'ballast'
    LOADED = 'loaded'

    VOYAGE_TYPE = [
        (BALLAST, 'Ballast leg'),
        (LOADED, 'Laden leg'),
    ]

    voyage_num = models.CharField(max_length=15)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=VOYAGE_TYPE, default=BALLAST)
    departure = models.ManyToManyField(SeaPort, through='DeparturePort', related_name='departure_port')
    destination = models.ManyToManyField(SeaPort, through='DestinationPort', related_name='arrival_port')

    def __str__(self):
        return f'{self.vessel} - {self.voyage_num}: {self.type}'

    @admin.display(description='vessel')
    def get_vessel(self):
        return self.vessel


class DestinationPort(models.Model):
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    seaport = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    eta = models.DateTimeField()
    arrival_date_time = models.DateTimeField(null=True, blank=True)
    utc_offset = models.FloatField(null=True, blank=True)


class DeparturePort(models.Model):
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    seaport = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    departure_date_time = models.DateTimeField()
    utc_offset = models.FloatField(null=True, blank=True)


class CargoType(models.Model):
    name = models.CharField(max_length=100)
    imo_class = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CargoOps(models.Model):
    LOADING = 'loading'
    DISCHARGING = 'discharging'

    CARGO_OPS_TYPES = [
        (LOADING, 'Loading'),
        (DISCHARGING, 'Discharging'),
    ]

    ops_date_time = models.DateTimeField(verbose_name='date time UTC')
    utc_offset = models.FloatField()
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    cargo_type = models.ForeignKey(CargoType, on_delete=models.CASCADE)
    operation = models.CharField(max_length=15, choices=CARGO_OPS_TYPES, default=LOADING)
    quantity = models.FloatField()
    bl_number = models.CharField(max_length=30)
    shipper = models.CharField(max_length=70)
    consignee = models.CharField(max_length=70)

    def __str__(self):
        return f'{self.voyage} - {self.operation}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['voyage', 'cargo', 'ops_date_time'], name='unique_cargo_ops')
        ]
        verbose_name = 'cargo operation'

    @admin.display(description='voyage')
    def get_voyage(self):
        return self.voyage


class BunkerType(models.Model):
    type = models.CharField(max_length=20, unique=True)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['type']


class BunkerOps(models.Model):
    ops_date_time = models.DateTimeField()
    utc_offset = models.FloatField()
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, null=True, blank=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    location = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    bunker = models.ForeignKey(BunkerType, on_delete=models.CASCADE)
    supplier = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'bunker operation'


class VesselPositionReport(models.Model):
    AT_SEA = 'sea'
    IN_PORT = 'port'
    DRIFTING = 'drifting'
    ANCHORAGE = 'anchorage'

    VESSEL_OPERATION = [
        (AT_SEA, 'Vessel is at sea'),
        (IN_PORT, 'Vessel is in port'),
        (DRIFTING, 'Vessel is drifting'),
        (ANCHORAGE, 'Vessel is at anchorage'),
    ]

    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, verbose_name='Voyage Number')
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    report_date_time = models.DateTimeField()
    utc_offset = models.FloatField()
    current_position = models.CharField(max_length=25)
    operation = models.CharField(max_length=15, choices=VESSEL_OPERATION, default=AT_SEA)
    distance_daily = models.PositiveIntegerField()
    speed_avg = models.PositiveIntegerField()
    course_avg = models.PositiveIntegerField()
    sea_bft = models.PositiveIntegerField()
    swell_bft = models.PositiveIntegerField()
    swell_dir = models.PositiveIntegerField()
    wind_bft = models.PositiveIntegerField()
    wind_dir = models.PositiveIntegerField()
    bunker = models.ManyToManyField(BunkerType, through='BunkerReport')

    class Meta:
        ordering = ['voyage', 'report_date_time']
        constraints = [
            models.UniqueConstraint(fields=['voyage', 'vessel', 'report_date_time'], name='unique_report')
        ]


class BunkerReport(models.Model):
    vessel_position = models.ForeignKey(VesselPositionReport, on_delete=models.CASCADE)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    bunker = models.ForeignKey(BunkerType, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        verbose_name = 'Daily bunker report'

