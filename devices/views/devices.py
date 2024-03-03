# Permissions
from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

#Serializers
from devices import models
from devices import serializers
from stats.models.history import History

# Utils
from utils.viewsets import BaseViewSet, logger


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
        device_exists =  True if History.objects.filter(host=instance.ip_address).count() else False

        if device_exists:
            instance.active = False
            instance.save()
        else:
            instance.delete()


    def destroy(self, request, *args, **kwargs):
        device_id = kwargs.get('pk')
        try:
            instance = self.model_class.objects.get(id=device_id)
        except self.model_class.DoesNotExist:
            instance = self.get_object()

        self.perform_destroy(instance)
        cache.delete_pattern(f"/{request.resolver_match.route.split('(?P')[0]}*")
        logger.info('Cache was cleaned successfully')
        return Response(status=status.HTTP_204_NO_CONTENT)
