# Django
from django.contrib import admin

# Models
from devices.models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass
