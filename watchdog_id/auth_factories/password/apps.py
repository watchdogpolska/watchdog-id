from __future__ import unicode_literals

from django.apps import AppConfig

from watchdog_id.auth_factories import Registry


class PasswordConfig(AppConfig):
    name = 'watchdog_id.auth_factories.password'

    def ready(self):
        from .config import PasswordConfig as cfg
        Registry[cfg.id] = cfg()
