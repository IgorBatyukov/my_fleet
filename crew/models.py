from django.contrib import admin
from django.db import models
from django.urls import reverse
from fleet.models import Vessel
from geo.models import City, EducationCenter, MedicalCenter, SeaPort
from personnel.models import Employee


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

    @admin.display(description='rank')
    def get_rank(self):
        return self.rank

    @admin.display(description='certificate')
    def get_certificate(self):
        return self.certificate


class CrewMember(models.Model):

    AT_SEA = 'at_sea'
    AT_HOME = 'at_home'
    MARRIED = 'married'
    SINGLE = 'single'

    WORKING_STATUS = [
        (AT_SEA, 'Sailor is on the vessel'),
        (AT_HOME, 'Sailor is on vacation'),
    ]

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
    working_status = models.CharField(max_length=10, choices=WORKING_STATUS, default=AT_HOME)
    certificates = models.ManyToManyField(Certificate, through='CrewCertification')
    medical_center = models.ManyToManyField(MedicalCenter, through='CrewMedicalExamination')
    education_center = models.ManyToManyField(EducationCenter, through='CrewEducation')
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} {self.surname} - {self.rank}'

    # def get_rank(self):
    #     return ','.join(
    #         [
    #             rank for rank in self.rank.filter(crewposition__hired_to__isnull=True)
    #             .values_list('name', flat=True).all()
    #         ]
    #     )
    #
    # def get_vessel(self):
    #     return ','.join(
    #         [
    #             vsl for vsl in self.vessel.filter(crewchange__signed_off__isnull=True)
    #             .values_list('name', flat=True).all()
    #         ]
    #     )


class CrewCertification(models.Model):
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    cert = models.ForeignKey(Certificate, on_delete=models.CASCADE)
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


class CrewEducation(models.Model):
    education_center = models.ForeignKey(EducationCenter, on_delete=models.CASCADE)
    crew_member = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    joined_date = models.DateField()
    graduated_date = models.DateField(null=True, blank=True)


class CrewChange(models.Model):
    crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    signed_on_date = models.DateField()
    signed_off_date = models.DateField(null=True, blank=True)
    signed_on_port = models.ForeignKey(SeaPort, on_delete=models.CASCADE, related_name='join_port')
    signed_off_port = models.ForeignKey(SeaPort,
                                        null=True,
                                        blank=True,
                                        on_delete=models.CASCADE,
                                        related_name='leave_port')
    manager = models.ForeignKey(Employee, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.crew} - {self.vessel}'

    class Meta:
        verbose_name = 'crew change'
        constraints = [
            models.UniqueConstraint(fields=['crew', 'signed_on_date', 'signed_on_port'], name='unique_crew_change')
        ]


# class CrewPosition(models.Model):
#     crew = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
#     rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
#     hired_from = models.DateField()
#     hired_to = models.DateField(null=True, blank=True)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['crew', 'hired_from'], name='unique_hire')
#         ]
#
#     def get_crew(self):
#         return self.crew
#
#     def get_rank(self):
#         return self.rank


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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['crew', 'signed_date'], name='unique_contract')
        ]

    def get_crew(self):
        return self.crew


class VesselsSchedule(models.Model):
    vessel_id = models.IntegerField()
    vessel_name = models.CharField(max_length=25)
    fleet = models.CharField(max_length=30)
    departure_port = models.CharField(max_length=50)
    destination_port = models.CharField(max_length=50)
    eta = models.DateTimeField()
    agency = models.CharField(max_length=50)
    type = models.CharField(max_length=10)
    voyage_num = models.CharField(max_length=15)
    operation = models.CharField(max_length=15)
    report_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'vessels_schedule'

    def get_absolute_url(self):
        return reverse('vessel_details', kwargs={'pk': self.vessel_id})


