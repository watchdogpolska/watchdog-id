from django.apps import AppConfig

from watchdog_id.auth_factories import Registry


class RecoveryMailConfig(AppConfig):
    name = 'watchdog_id.auth_factories.recovery_mail'

    def ready(self):
        from .factory import RecoveryMailFactory as cfg
        Registry[cfg.id] = cfg()
