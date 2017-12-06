from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthLocalLogConfig(AppConfig):
    name = 'watchdog_id.auth_local_log'
    verbose_name = _("Auth local logs")

    def ready(self):
        from . import signals
