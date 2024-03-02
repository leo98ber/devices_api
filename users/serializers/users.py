# Django
from django.contrib.auth import password_validation
from django.core.validators import EmailValidator

# Django REST Framework
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# MODELS
from users.models import User

# SERIALIZERS
from rest_framework import serializers



class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class."""

        model = User
        exclude = ['password', 'is_staff', 'groups', 'user_permissions']




class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation and user/profile creation.
    """

    email = serializers.CharField(
        validators=[
            EmailValidator(),
            UniqueValidator(queryset=User.objects.all(), message='Este correo electrónico ya está en uso.')
        ]
    )


    username = serializers.CharField(
        min_length=1,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30, allow_blank=True)
    last_name = serializers.CharField(min_length=2, max_length=30, allow_blank=True)


    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError({'password': "Las contraseñas no coinciden."})
        try:
            password_validation.validate_password(passwd)
        except Exception as ex:
            raise serializers.ValidationError({"password": ' '.join(ex.messages)})

        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)

        return user

    class Meta:
        model = User
        fields = '__all__'



class UserLoginSerializer(TokenObtainPairSerializer):
    """Generate Json web toke from TokenObtainPairSerializer"""
