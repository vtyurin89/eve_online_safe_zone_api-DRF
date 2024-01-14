from django.db.models import Sum
from rest_framework import serializers

from .models import System, DangerRating
from .base_constants import MAX_HOURS_LIMIT


class SystemSerializer(serializers.ModelSerializer):
    danger_rating = serializers.IntegerField()

    class Meta:
        model = System
        fields = '__all__'

    # def get_danger_rating(self, obj):
    #     danger_rating = DangerRating.objects.filter(system=obj)\
    #         .order_by('-timestamp')[:MAX_HOURS_LIMIT].aggregate(Sum('value'))
    #     return danger_rating['value__sum']



