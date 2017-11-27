# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from watchdog_id.auth_factories import Registry


class YubicoOtpConfig(AppConfig):
    name = 'watchdog_id.auth_factories.yubico_otp'

    def ready(self):
        from .factory import YubicoOtpFactory as f
        Registry[f.id] = f()
