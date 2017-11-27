from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.config import BaseConfig


class ConsoleOtpConfig(BaseConfig):
    id = 'console_otp'
    urlpatterns = 'watchdog_id.auth_factories.console_otp.urls'
    name = _("Console OTP")
    weight = 50

    def is_available(self, user):
        return settings.DEBUG

    def is_enabled(self, user):
        return settings.DEBUG

    def get_settings_url(self):
        return None
