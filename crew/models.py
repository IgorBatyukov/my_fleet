from datetime import datetime as dt
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, Q
from django.urls import reverse
from fleet.models import Vessel, Fleet, VesselType
from geo.models import City, EducationCenter, MedicalCenter, SeaPort
from operations.models import Agency
from personnel.models import Employee


class Rank(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Certificate(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CertificationMatrix(models.Model):
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    vessel_type = models.ForeignKey(VesselType, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['rank', 'certificate', 'vessel_type'], name='unique_requirement')
        ]
        verbose_name_plural = 'certification matrix'

    def __str__(self):
        return f'{self.certificate} for {self.rank} on {self.vessel_type}'

    @classmethod
    def get_vessel_type_list(cls):
        return cls.objects.values_list('vessel_type__name', flat=True).distinct()


class CrewMember(models.Model):
    AT_SEA = 'Sailor is on the vessel'
    AT_HOME = 'Sailor is on vacation'
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
    certificates = models.ManyToManyField(Certificate, through='CrewCertification')
    medical_center = models.ManyToManyField(MedicalCenter, through='CrewMedicalExamination')
    education_center = models.ManyToManyField(EducationCenter, through='CrewEducation')
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
    fleet = models.ForeignKey(Fleet, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['rank', 'name']

    def __str__(self):
        return f'{self.name} {self.surname} - {self.rank}'

    @property
    def get_certificates(self):
        return self.crewcertification_set.all()

    @property
    def get_medical_examination(self):
        for examination in self.crewmedicalexamination_set.all():
            return examination if examination.is_valid else None

    @property
    def get_education_info(self):
        pass

    @property
    def get_working_status(self):
        return self.AT_SEA if self.pk in CrewOnBoard.objects.values_list('id', flat=True) else self.AT_HOME

    @property
    def get_vessel(self):
        if self.get_working_status == self.AT_SEA:
            return CrewOnBoard.objects.get(id=self.pk).vsl_name
        return None


class CrewCertification(models.Model):
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    cert = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    cert_number = models.CharField(max_length=20, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cert_id', 'cert_number'], name='unique_certificate')
        ]

    def __str__(self):
        return f'{self.cert} for {self.crew}'

    @classmethod
    def get_certificates_for_sailor(cls, sailor):
        return cls.objects.filter(crew=sailor).values_list('cert', flat=True)

    def clean(self):
        if self.valid_from >= self.valid_to and self.valid_to:
            raise ValidationError('Date of issuance can not be greater than date of expiration')
        super().clean()


class CrewMedicalExamination(models.Model):
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    med_center = models.ForeignKey(MedicalCenter, on_delete=models.DO_NOTHING)
    valid_from = models.DateField()
    valid_to = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['crew', 'valid_from'], name='unique_examination')
        ]

    def __str__(self):
        return f'{self.crew} at {self.med_center} ({self.valid_from} - {self.valid_to})'

    @property
    def is_valid(self):
        today = dt.today().date()
        return True if self.valid_to > today else False


class CrewEducation(models.Model):
    education_center = models.ForeignKey(EducationCenter, on_delete=models.CASCADE)
    crew_member = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    joined_date = models.DateField()
    graduated_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.crew_member} at {self.education_center} ({self.joined_date} - {self.graduated_date})'


class CrewChange(models.Model):
    JOIN = 'join'
    LEAVE = 'leave'

    CHANGE_TYPE = [
        (JOIN, 'joining'),
        (LEAVE, 'leaving')
    ]

    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    date = models.DateField()
    port = models.ForeignKey(SeaPort, on_delete=models.CASCADE)
    type = models.CharField(max_length=5, choices=CHANGE_TYPE, default=JOIN)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    manager = models.ForeignKey(Employee, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'crew change'
        constraints = [
            models.UniqueConstraint(fields=['crew', 'vessel', 'date', 'type'], name='unique_crew_change')
        ]

    def __str__(self):
        return f'{self.crew} - {self.vessel}'

    def clean(self):
        crew_id = self.crew_id
        vessel_id = self.vessel_id
        if not Contract.objects.filter(
                Q(crew_id=crew_id) &
                Q(vessel_id=vessel_id) &
                Q(finished_date__isnull=True)).exists():
            raise ValidationError('Cannot assign a crew change for a crew member without a signed contract')
        super().clean()

    @classmethod
    def get_crew_changes_list(cls):
        return cls.objects.values('vessel__name',
                                  'date',
                                  'port__name',
                                  'type').annotate(crew=Count('crew')).order_by('-date')


class SalaryMatrix(models.Model):
    rank = models.OneToOneField(Rank, on_delete=models.CASCADE)
    basic = models.FloatField()
    performance_bonus = models.FloatField()
    leave_payment = models.FloatField()

    class Meta:
        verbose_name_plural = 'salary matrix'
        ordering = ['rank']

    def get_rank(self):
        return self.rank

    def get_total(self):
        return self.basic + self.performance_bonus + self.leave_payment


class Contract(models.Model):
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    duration = models.SmallIntegerField()
    offset = models.SmallIntegerField()
    signed_date = models.DateField()
    finished_date = models.DateField(null=True, blank=True)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['crew', 'signed_date'], name='unique_contract')
        ]


class CrewOnBoard(models.Model):
    """
    Materialized view model for aggregated data related to crew members who are currently at sea
    """
    crew_name = models.CharField(max_length=150)
    rank_id = models.SmallIntegerField()
    rank = models.CharField(max_length=20)
    vsl_id = models.SmallIntegerField()
    vsl_name = models.CharField(max_length=25)
    contract_signed = models.DateField()
    contract_exp = models.DateField()
    offset = models.SmallIntegerField()
    joined_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'crew_onboard'

    def get_absolute_url(self):
        return reverse('crew_member_details', kwargs={'pk': self.pk})


class CrewList(models.Model):
    """
    Materialized view model for aggregated data related to crew members current status and their last contract
    """
    crew_name = models.TextField()
    rank_id = models.SmallIntegerField()
    rank = models.CharField(max_length=20)
    working_status = models.CharField(max_length=30)
    vessel_name = models.CharField(max_length=25)
    fleet_id = models.SmallIntegerField()
    fleet_name = models.CharField(max_length=30)
    signed_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'crew_list'

    def get_absolute_url(self):
        return reverse('crew_member_details', kwargs={'pk': self.id})
