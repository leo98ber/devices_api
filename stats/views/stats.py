from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_mongoengine.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from settings import logger
from stats.models import Latency
from stats.models.history import History
from stats.pipelines import HISTORY_STATS_PIPELINE, CURRENT_STATS_PIPELINE
from utils.errors import DataSourceEmpty


class DashBoardViewSet(GenericViewSet):
    def get_permissions(self):
        return [IsAuthenticated()]

    @action(methods=['post'], detail=False)
    def get_stats(self, request):
        data = {}
        try:
            device = request.data.get('device')

            if device:
                filter_query = {'host': device}
            else:
                filter_query = {}

            var_to_convert = ['total_tests', 'total_error_tests', 'total_success_tests',
                              'current_latency_average',
                              'current_errors',
                              'current_success'
                              ]
            history_data = list(History.objects(**filter_query).aggregate(HISTORY_STATS_PIPELINE))[0]
            current_device_data = list(Latency.objects(**filter_query).aggregate(CURRENT_STATS_PIPELINE))[0]

            for each in var_to_convert:
                if each in history_data:
                    history_data[each] = history_data.pop(each, {})
                elif each in current_device_data:
                    current_device_data[each] = current_device_data.pop(each, {})

            data.update(history_data)
            data.update(current_device_data)

            if not data:
                raise DataSourceEmpty('Empty data for request parameters')

            response_status = status.HTTP_200_OK

        except DataSourceEmpty as ex1:
            logger.error(f"{str(ex1)}")
            data = {'content': {}}
            response_status = status.HTTP_204_NO_CONTENT

        except Exception as ex:
            logger.error(f"Unexpected error fetching select data: {ex}")
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            data = {'content': None}

        return Response({'content': data}, response_status)

