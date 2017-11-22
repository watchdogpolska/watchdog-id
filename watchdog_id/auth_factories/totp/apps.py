# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from watchdog_id.auth_factories import Registry


class TotpConfig(AppConfig):
    name = 'watchdog_id.auth_factories.totp'

    def ready(self):
        from .factory import TOTPFactory as factory
        Registry[factory.id] = factory()
