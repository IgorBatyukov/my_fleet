from django.db import models


class Fleet(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def get_vessels(self):
        return list(self.vessel_set.all())


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
    former_name = models.CharField(max_length=25, null=True, blank=True)
    fleet = models.ForeignKey(Fleet, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(VesselType, on_delete=models.CASCADE)
    imo = models.IntegerField(unique=True)
    length = models.SmallIntegerField()
    breadth = models.SmallIntegerField()
    grt = models.IntegerField()
    nrt = models.IntegerField()
    flag = models.ForeignKey(VesselFlag, on_delete=models.SET_NULL, null=True, blank=True)
    class_society = models.ForeignKey(ClassSociety, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def get_fleet(self):
        return self.fleet
