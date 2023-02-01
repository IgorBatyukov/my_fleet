from django.db import models


class Fleet(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def get_vessels(self):
        return self.vessel_set.all()


class VesselType(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class VesselFlag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ClassSociety(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.short_name


class Vessel(models.Model):
    name = models.CharField(max_length=25, unique=True)
    fleet = models.ForeignKey(Fleet, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(VesselType, on_delete=models.DO_NOTHING)
    imo = models.IntegerField(unique=True)
    length = models.SmallIntegerField()
    breadth = models.SmallIntegerField()
    grt = models.IntegerField()
    nrt = models.IntegerField()
    flag = models.ForeignKey(VesselFlag, on_delete=models.DO_NOTHING)
    class_society = models.ForeignKey(ClassSociety, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def get_fleet(self):
        return self.fleet
