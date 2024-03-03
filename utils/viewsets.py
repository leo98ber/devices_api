# Python
import logging

# Django
from django.core.cache import cache

# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Decorators
from utils.decorators import calculate_time_process

logger = logging.getLogger('console')


class BaseAPIMixin(viewsets.GenericViewSet):
    methods_parameters: dict = {}
    query_parameters: dict = {}
    list_keys: list = []
    model_class = None
    def get_permissions(self):
        list_permissions = self.methods_parameters.get(self.action, {}).get('permissions')

        if list_permissions:
            return [permission() for permission in list_permissions if not None]

        else:
            return [IsAuthenticated()]

    def get_serializer_class(self):
        """Return serializer based on action."""
        return self.methods_parameters.get(self.action, {}).get('serializer', self.serializer_class)

    @calculate_time_process
    def get_queryset(self):
        query_set = self.model_class.objects.filter(**self.query_parameters)
        return query_set

    def add_context(self, data):
        context: dict = {}
        for each, init_type in self.list_keys:
            context[each] = data.pop(each, init_type)
        return context, data

    def add_user_to_request(self, request, data, field):
        model_as_dict = self.serializer_class.Meta.model.__dict__
        if field in model_as_dict:
            data[field] = request.user.pk
        return data




class CreateViewSet(mixins.CreateModelMixin, BaseAPIMixin):

    def perform_create(self, serializer):
        super().perform_create(serializer)
        return serializer.data

    def create(self, request, *args, **kwargs):
        data = request.data
        data = self.add_user_to_request(request, data, 'created_by')
        context, data = self.add_context(data)
        context['session'] = request.session
        serializer = self.get_serializer(data=data,
                                         context=context)

        serializer.is_valid(raise_exception=True)
        return_data = self.perform_create(serializer)
        headers = self.get_success_headers(return_data)
        cache.delete_pattern(f'{request.path}*')
        logger.info('Cache was cleaned successfully')
        return Response(return_data, status=status.HTTP_201_CREATED, headers=headers)

class UpdateViewSet(mixins.UpdateModelMixin, BaseAPIMixin):
    def perform_update(self, serializer):
        super().perform_update(serializer)
        return serializer.data

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        data = self.add_user_to_request(request, data, 'modified_by')
        context, data = self.add_context(data)
        context['session'] = request.session
        serializer = self.get_serializer(instance, data=data,
                                         partial=partial, context=context)
        serializer.is_valid(raise_exception=True)
        return_data = self.perform_update(serializer)
        cache.delete_pattern(f"/{request.resolver_match.route.split('(?P')[0]}*")
        logger.info('Cache was cleaned successfully')

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(return_data)


class ListViewSet(mixins.ListModelMixin, BaseAPIMixin):
    ordering = None
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)


    def list(self, request, *args, **kwargs):
        query_params = request.GET.items()
        view_set_url = request.path
        if query_params:
            view_set_url = view_set_url + '?'
            for key,value in query_params:
                view_set_url = view_set_url + key + '/' + value
        response_data = cache.get(view_set_url)

        if not response_data:
            response_instance = super().list(request, *args, **kwargs)
            response_data = response_instance.data
            cache.set(view_set_url, response_data)
        return Response(response_data)


class RetrieveViewSet(mixins.ListModelMixin, BaseAPIMixin):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'session': request.session})
        edit_enable = request.session.get('edit_enable', False)
        response_data = serializer.data
        response_data['edit_enable'] = edit_enable
        return Response(response_data)

class DestroyViewSet(mixins.DestroyModelMixin, BaseAPIMixin):

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        cache.delete_pattern(f"/{request.resolver_match.route.split('(?P')[0]}*")
        logger.info('Cache was cleaned successfully')
        return Response(status=status.HTTP_204_NO_CONTENT)

class BaseViewSet(viewsets.ModelViewSet,
                    CreateViewSet,
                    UpdateViewSet,
                    ListViewSet,
                    RetrieveViewSet,
                    DestroyViewSet):

    pass












