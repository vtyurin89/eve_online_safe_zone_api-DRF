from django.db import models


# class System(models.Model):
#     system_id = models.UUIDField(primary_key=True, editable=False)
#     name = models.CharField(max_length=60)
#     security_class = models.CharField(max_length=60)
#     system_security = models.FloatField()
#     position = models.ForeignKey('XYZ', on_delete=models.CASCADE)
#     star = models.ForeignKey('Star', on_delete=models.CASCADE)
#
#
# class Star(models.Model):
#     star_id = models.UUIDField(primary_key=True, editable=False)
#     name = models.CharField(max_length=60)
#
#
# class Stargate(models.Model):
#     stargate_id = models.UUIDField(primary_key=True, editable=False)
#     name = models.CharField(max_length=60)
#     system = models.ForeignKey('System', on_delete=models.CASCADE)
#
#
# class Station(models.Model):
#     station_id = models.UUIDField(primary_key=True, editable=False)
#     name = models.CharField(max_length=60)
#     system = models.ForeignKey('System', on_delete=models.CASCADE)


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


#
# class SolarSystem(models.Model):
#     regionid = models.IntegerField(db_column='regionID', blank=True, null=True)
#     constellationid = models.IntegerField(db_column='constellationID', blank=True, null=True)
#     solarsystemid = models.IntegerField(db_column='solarSystemID', primary_key=True)
#     solarsystemname = models.CharField(db_column='solarSystemName', max_length=100, blank=True, null=True)
#     x = models.FloatField(blank=True, null=True)
#     y = models.FloatField(blank=True, null=True)
#     z = models.FloatField(blank=True, null=True)
#     xmin = models.FloatField(db_column='xMin', blank=True, null=True)
#     xmax = models.FloatField(db_column='xMax', blank=True, null=True)
#     ymin = models.FloatField(db_column='yMin', blank=True, null=True)
#     ymax = models.FloatField(db_column='yMax', blank=True, null=True)
#     zmin = models.FloatField(db_column='zMin', blank=True, null=True)
#     zmax = models.FloatField(db_column='zMax', blank=True, null=True)
#     luminosity = models.FloatField(blank=True, null=True)
#     border = models.IntegerField(blank=True, null=True)
#     fringe = models.IntegerField(blank=True, null=True)
#     corridor = models.IntegerField(blank=True, null=True)
#     hub = models.IntegerField(blank=True, null=True)
#     international = models.IntegerField(blank=True, null=True)
#     regional = models.IntegerField(blank=True, null=True)
#     constellation = models.IntegerField(blank=True, null=True)
#     security = models.FloatField(blank=True, null=True)
#     factionid = models.IntegerField(db_column='factionID', blank=True, null=True)
#     radius = models.FloatField(blank=True, null=True)
#     suntypeid = models.IntegerField(db_column='sunTypeID', blank=True, null=True)
#     securityclass = models.CharField(db_column='securityClass', max_length=2, blank=True, null=True)
#
#     class Meta:
#         db_table = 'mapsolarsystems'
