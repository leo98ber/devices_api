# Permissions
from rest_framework.permissions import IsAuthenticated

#Serializers
from devices import models
from devices import serializers

# Utils
from utils.viewsets import BaseViewSet


class DeviceViewSet(BaseViewSet):
    serializer_class = serializers.DeviceSerializer
    model_class = models.Device

    methods_parameters: dict = {

                                'create': {'permissions': [IsAuthenticated]},


                                'update': {'permissions': [IsAuthenticated]},

                                'partial_update': {'permissions': [IsAuthenticated]},

                                'list': {'serializer': serializers.DeviceListSerializer,
                                         'permissions': [IsAuthenticated]},

                                'retrieve': {'permissions': [IsAuthenticated]},

                                'destroy': {'permissions': [IsAuthenticated]},


                                }

    query_parameters = {'active': True}

    # Filters
    search_fields = ('name', 'code', 'ip_address', 'created_by__username')

    ordering_fields = ('name', 'code')
    ordering = ('-name',)

    filter_fields = search_fields
    def perform_destroy(self, instance):
        # test_ip_direction = True
        # if test_ip_direction:
        #     instance.active = False
        #     instance.save()
        # else:
        instance.delete()

