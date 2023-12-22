from django.db import models


class Stargate(models.Model):
    stargate_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    system = models.ForeignKey('System', on_delete=models.CASCADE)


class Station(models.Model):
    station_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    system = models.ForeignKey('System', on_delete=models.CASCADE)


class Region(models.Model):
    regionid = models.IntegerField(primary_key=True)
    description = models.TextField(max_length=10000)
    name = models.CharField(max_length=60)


class Constellation(models.Model):
    constellationid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)


class System(models.Model):
    constellation = models.ForeignKey("Constellation", on_delete=models.CASCADE, null=True, blank=True)
    system_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    security_class = models.CharField(max_length=2, blank=True, null=True)
    security_status = models.FloatField(blank=True, null=True)


