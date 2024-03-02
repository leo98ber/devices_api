# Django
from django.contrib.auth import authenticate
from django.core.cache import cache

# Django Rest Framework
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated

#Serializers
from users import models
from users import serializers

# Utils
from utils.viewsets import BaseViewSet


# Others
from datetime import datetime


class UserViewSet(BaseViewSet):
    serializer_class = serializers.UserModelSerializer
    model_class = models.User
    basename = 'users'
    methods_parameters: dict = {

                                'create': {'serializer': serializers.UserSignUpSerializer,
                                           'permissions': [IsAuthenticated]},

                                'logout': {'serializer': serializers.UserSignUpSerializer,
                                           'permissions': [IsAuthenticated]},

                                'signup': {'serializer': serializers.UserSignUpSerializer,
                                           'permissions': [AllowAny]},

                                'login': {'serializer': serializers.UserLoginSerializer,
                                          'permissions': [AllowAny]},

                                'update': {'permissions': [IsAuthenticated]},

                                'partial_update': {'permissions': [IsAuthenticated]},

                                'list': {'serializer': serializers.UserListSerializer,
                                         'permissions': [IsAuthenticated]},

                                'retrieve': {'permissions': [IsAuthenticated]},

                                'destroy': {'permissions': [IsAuthenticated]},


                                }

    # query_parameters = {'is_active': True}

    # Filters
    search_fields = ('username', 'first_name', 'last_name', 'email', 'is_active')

    ordering_fields = ('username', 'first_name', 'last_name', 'email')  # Order options
    ordering = ('-username',)  # Default order

    filter_fields = search_fields

    def perform_create(self, serializer):
        user = serializer.save()
        return serializers.UserModelSerializer(user).data
    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""

        create_result = self.create(request)
        cache.delete_pattern(f"{request.path.replace('signup/', '')}*")
        return create_result

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""

        login_error = {'message': 'Contraseña o nombre de usuario incorrectos'}
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        user = authenticate(
            email=email,
            password=password
        )

        if user:
            login_serializer = self.get_serializer(data=request.data)
            if login_serializer.is_valid():
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'username': user.username,
                        'email': user.email
                    },

                    'message': 'Inicio de Sesion Existoso'
                }, status=status.HTTP_200_OK)

        return Response(login_error, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def logout(self, request, *args, **kwargs):
        user = self.model_class.objects.filter(id=request.user.id)
        refresh_token = request.data.get('refresh_token')

        if user.exists():
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            else:
                tokens = OutstandingToken.objects.filter(user_id=request.user.id,
                                                         expires_at__gte=datetime.now())
                for token in tokens:
                    BlacklistedToken.objects.get_or_create(token=token)

            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_205_RESET_CONTENT)
        return Response({'message': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], url_path='change_password', detail=False)
    def change_password(self, request):
        data = request.data
        serializer = serializers.ChangePasswordSerializer(data=data)
        serializer.context['user'] = request.user
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_status = status.HTTP_200_OK
        data = {'message': 'Cambio de contraseña exitoso.'}
        return Response(data,
                        status=response_status)

