from django.db import models


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

    def get_city(self):
        return self.city


class SeaPort(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.name}, {self.country}'

    class Meta:
        ordering = ['name']

    def get_country(self):
        return self.country


class EducationCenter(models.Model):
    name = models.CharField(max_length=200, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_location(self):
        return self.city


class MedicalCenter(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_location(self):
        return self.city


class Shipyard(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_city(self):
        return self.city

    def get_country(self):
        return self.country

