# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from watchdog_id.auth_factories import Registry


class ConsoleOtpConfig(AppConfig):
    name = 'watchdog_id.auth_factories.console_otp'

    def ready(self):
        from .config import ConsoleOtpConfig as cfg
        Registry[cfg.id] = cfg()
