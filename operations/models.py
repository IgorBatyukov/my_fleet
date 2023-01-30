from django.db import models
from fleet.models import Vessel
from geo.models import SeaPort


class Agency(models.Model):
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
    BALLAST = 'ballast'
    LOADED = 'loaded'

    VOYAGE_TYPE = [
        (BALLAST, 'Ballast leg'),
        (LOADED, 'Laden leg'),
    ]

    voy_num = models.CharField(max_length=15)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=VOYAGE_TYPE, default=BALLAST)
    departure = models.ForeignKey(SeaPort, on_delete=models.CASCADE, related_name='departure_port')
    destination = models.ManyToManyField(SeaPort, related_name='destination_port')
    eta = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    agency = models.ManyToManyField(Agency)


class Cargo(models.Model):
    CRUDE_OIL = 'crude_oil'
    FUEL_OIL = 'fuel_oil'
    DIESEL_OIL = 'diesel_oil'
    GRAIN_BULK = 'grain_bulk'
    COAL_BULK = 'coal_bulk'
    GENERAL_CARGO = 'general_cargo'

    CARGO_TYPES = [
        (CRUDE_OIL, 'Crude Oil'),
        (FUEL_OIL, 'Fuel Oil'),
        (DIESEL_OIL, 'Diesel Oil'),
        (GRAIN_BULK, 'Grain in Bulk'),
        (COAL_BULK, 'Coal in Bulk'),
        (GENERAL_CARGO, 'General Cargo'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CARGO_TYPES, default=CRUDE_OIL)
    vessel = models.ManyToManyField(Vessel)

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

    ops_date_time = models.DateTimeField()
    utc_offset = models.FloatField()
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    cargo = models.OneToOneField(Cargo, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=CARGO_OPS_TYPES, default=LOADING)
    quantity = models.FloatField()
    bl_number = models.CharField(max_length=30)
    shipper = models.CharField(max_length=70)
    consignee = models.CharField(max_length=70)

    def __str__(self):
        return f'{self.vessel} - {self.type}: {self.ops_date_time}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vessel', 'cargo', 'ops_date_time'], name='unique_cargo_ops')
        ]


class Bunker(models.Model):
    FUEL_OIL = 'FO'
    DIESEL_OIL = 'DO'
    MARINE_GAS_OIL = 'MGO'
    VERY_LOW_SULPHUR_FUEL_OIL = 'VLSFO'

    BUNKER_TYPES = [
        (FUEL_OIL, 'Fuel Oil'),
        (DIESEL_OIL, 'Diesel Oil'),
        (MARINE_GAS_OIL, 'Marine Gas Oil'),
        (VERY_LOW_SULPHUR_FUEL_OIL, 'Very Low Sulphur Fuel Oil'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=BUNKER_TYPES, default=DIESEL_OIL)
    vessel = models.ManyToManyField(Vessel)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class BunkerOps(models.Model):
    ops_date_time = models.DateTimeField()
    utc_offset = models.FloatField()
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    location = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    bunker = models.ForeignKey(Bunker, on_delete=models.CASCADE)
    supplier = models.CharField(max_length=100)


class VesselPosition(models.Model):
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

    voy_num = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    report_date = models.DateField()
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

