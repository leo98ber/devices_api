# Python
import logging

# Django
from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password

# Django Rest Framework
from rest_framework import serializers

logger = logging.getLogger('console')

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)

    def validate(self, data):
        old_password = data["old_password"]
        new_password = data["new_password"]
        new_password_confirmation = data["new_password_confirmation"]

        if not self.context["user"].check_password(raw_password=old_password):
            logger.error(f'Validation error in ChangePasswordSerializer: username/old password is incorrect')
            raise serializers.ValidationError("Usuario o contraseña incorrecta.")

        if new_password != new_password_confirmation:
            logger.error(f'Validation error in ChangePasswordSerializer: '
                         f'new password and new password confirmation do not match')
            raise serializers.ValidationError("Las contraseñas no coinciden.")

        try:
            validate_password(password=new_password, user=self.context["user"])
        except Exception as e:
            logger.error(f'Error in ChangePasswordSerializer while validating password: {e}')
            raise

        self.context["password"] = new_password
        return data

    def save(self):
        try:
            password = self.context["password"]
            user = self.context["user"]
            user.set_password(password)
            # send_password_changed_notification(user.username)
            user.is_verified = True
            user.save()
            return user

        except Exception as e:
            logger.error(f'Error in ChangePasswordSerializer while saving: {e}')
            raise Exception(str(e))


