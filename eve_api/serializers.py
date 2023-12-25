from rest_framework import serializers

from .models import System


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ['system_id', 'constellation', 'name', 'x', 'y', 'z', 'security_class', 'security_status']


