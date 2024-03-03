#Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'
    verbose_name = _('Stats')

