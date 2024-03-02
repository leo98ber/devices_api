from django.db import models
from utils.models import TimeBaseModel


class Device(TimeBaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4', unique=True)
    created_by = models.ForeignKey('users.User', related_name='created_user',
                                   on_delete=models.SET_NULL, null=True)
    modified_by = models.ForeignKey('users.User', related_name='modified_user',
                                    on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name