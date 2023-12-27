from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q

from .base_constants import MAX_HOURS_LIMIT


RATING_MAX_VALUE = MAX_HOURS_LIMIT * 10


class Stargate(models.Model):
    stargate_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    system = models.ForeignKey('System', on_delete=models.CASCADE)

    class Meta:
        db_table = 'eve_api_stargate'


class Station(models.Model):
    station_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    system = models.ForeignKey('System', on_delete=models.CASCADE)

    class Meta:
        db_table = 'eve_api_station'


class Region(models.Model):
    regionid = models.IntegerField(primary_key=True)
    description = models.TextField(max_length=10000)
    name = models.CharField(max_length=60)

    class Meta:
        db_table = 'eve_api_region'


class Constellation(models.Model):
    constellationid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)

    class Meta:
        db_table = 'eve_api_constellation'


class System(models.Model):
    constellation = models.ForeignKey("Constellation", on_delete=models.CASCADE, null=True, blank=True)
    system_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    z = models.FloatField(blank=True, null=True)
    security_class = models.CharField(max_length=2, blank=True, null=True)
    security_status = models.FloatField(blank=True, null=True)
    _danger_level = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(RATING_MAX_VALUE)],
                    db_column='danger_level', default=0)
    days_researched = models.PositiveIntegerField(default=0, db_column='days_researched')

    @property
    def danger_level(self):
        return self._danger_level

    @danger_level.setter
    def danger_level(self, value):
        self._danger_level = max(0, min(value, RATING_MAX_VALUE))

    class Meta:
        db_table = 'eve_api_system'
        constraints = [
            models.CheckConstraint(
                check=Q(_danger_level__range=(0, RATING_MAX_VALUE)), name='range_of_danger_level'
            )
        ]




