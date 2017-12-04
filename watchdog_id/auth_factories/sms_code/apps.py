from django.apps import AppConfig

from watchdog_id.auth_factories import Registry


class SmsCodeConfig(AppConfig):
    name = 'watchdog_id.auth_factories.sms_code'

    def ready(self):
        from .factory import SmsCodeFactory as cfg
        Registry[cfg.id] = cfg()
