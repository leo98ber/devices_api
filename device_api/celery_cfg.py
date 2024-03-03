from __future__ import absolute_import, unicode_literals

import os

# from celery.schedules import crontab
from django.apps import AppConfig, apps

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "device_api.settings")

app = Celery("device_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

class CeleryAppConfig(AppConfig):
    name = 'tasks'
    verbose_name = 'Celery Config'

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


__all__ = ("app",)
