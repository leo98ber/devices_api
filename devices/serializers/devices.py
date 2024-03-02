# MODELS
from devices.models import Device

# SERIALIZERS
from rest_framework import serializers


class DeviceListSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Device
        exclude = ['active', 'modified_by', 'description', 'modified_on']


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = '__all__'

