# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from watchdog_id.auth_factories import Registry


class WatchdogU2FConfig(AppConfig):
    name = 'watchdog_id.auth_factories.watchdog_u2f'

    def ready(self):
        from .factory import WatchdogU2FFactory as factory
        Registry[factory.id] = factory()
