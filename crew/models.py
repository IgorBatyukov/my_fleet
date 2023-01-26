from django.db import models
from vessel.models import Vessel


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)
    iso_code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'countries'


class City(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
        ordering = ['name']

    def get_country(self):
        return self.country


class Airport(models.Model):
    name = models.CharField(max_length=30)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    iata_code = models.CharField(max_length=3)


class EducationCenter(models.Model):
    name = models.CharField(max_length=200, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_location(self):
        return self.city


class Rank(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Certificate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CertificationMatrix(models.Model):
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['rank', 'certificate'], name='unique_requirement')
        ]
        verbose_name_plural = 'certification matrix'

    def get_rank(self):
        return self.rank

    def get_certificate(self):
        return self.certificate


class MedicalCenter(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_location(self):
        return self.city


class CrewMember(models.Model):

    WORKING_STATUS = [
        ('at_sea', 'Sailor is on the vessel'),
        ('at_home', 'Sailor is on vacation'),
    ]

    MARRIAGE_STATUS = [
        ('married', 'Married'),
        ('single', 'Single'),
    ]

    name = models.CharField(max_length=15)
    father_name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=25)
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    marriage_status = models.CharField(max_length=7, choices=MARRIAGE_STATUS, default='single')
    education_center = models.ForeignKey(EducationCenter, on_delete=models.DO_NOTHING)
    is_graduated = models.BooleanField()
    graduated_date = models.DateField(null=True)
    working_status = models.CharField(max_length=10, choices=WORKING_STATUS, default='at_home')
    certificates = models.ManyToManyField(Certificate, through='CrewCertification')
    medical_center = models.ManyToManyField(MedicalCenter, through='CrewMedicalExamination')
    vessel = models.ManyToManyField(Vessel, through='CrewOnVessel')
    rank = models.ManyToManyField(Rank, through='CrewPosition', verbose_name='Rank')

    def __str__(self):
        return f'{self.name} {self.father_name} {self.surname}'

    def get_rank(self):
        return ','.join(
            [
                rank for rank in self.rank.filter(crewposition__hired_to__isnull=True)
                .values_list('name', flat=True).all()
            ]
        )

    def get_vessel(self):
        return ','.join(
            [
                vsl for vsl in self.vessel.filter(crewonvessel__signed_off__isnull=True)
                .values_list('name', flat=True).all()
            ]
        )


class CrewCertification(models.Model):
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    cert = models.ForeignKey(Certificate, on_delete=models.DO_NOTHING)
    cert_number = models.CharField(max_length=20, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cert_id', 'cert_number'], name='unique_certificate')
        ]

    def get_crew(self):
        return self.crew

    def get_certificate(self):
        return self.cert


class CrewMedicalExamination(models.Model):
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    med_center = models.ForeignKey(MedicalCenter, on_delete=models.DO_NOTHING)
    valid_from = models.DateField()
    valid_to = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['crew', 'valid_from'], name='unique_examination')
        ]

    def get_crew(self):
        return self.crew

    def get_medical_center(self):
        return self.med_center


class CrewOnVessel(models.Model):
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    vsl = models.ForeignKey(Vessel, on_delete=models.DO_NOTHING)
    signed_on = models.DateField()
    signed_off = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'crew change'
        constraints = [
            models.UniqueConstraint(fields=['crew', 'signed_on'], name='unique_crew_on_vsl')
        ]

    def get_crew(self):
        return self.crew

    def get_vessel(self):
        return self.vsl


class CrewPosition(models.Model):
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    rank = models.ForeignKey(Rank, on_delete=models.DO_NOTHING)
    hired_from = models.DateField()
    hired_to = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['crew', 'hired_from'], name='unique_hire')
        ]

    def get_crew(self):
        return self.crew

    def get_rank(self):
        return self.rank


class SalaryMatrix(models.Model):
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, unique=True)
    basic = models.IntegerField()
    performance_bonus = models.IntegerField()
    leave_payment = models.IntegerField()

    class Meta:
        verbose_name_plural = 'salary matrix'
        ordering = ['rank']

    def get_rank(self):
        return self.rank

    def get_total(self):
        return self.basic + self.performance_bonus + self.leave_payment


class Contract(models.Model):
    manager = models.IntegerField()
    crew = models.ForeignKey(CrewMember, on_delete=models.DO_NOTHING)
    duration = models.SmallIntegerField()
    offset = models.SmallIntegerField()
    signed_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['crew', 'signed_date'], name='unique_contract')
        ]

    def get_crew(self):
        return self.crew


