from django.utils.translation import ugettext_lazy as _
from watchdog_id.auth_factories.config import BaseConfig


class ConsoleOtpConfig(BaseConfig):
    id = 'console_otp'
    urlpatterns = 'watchdog_id.auth_factories.console_otp.urls'
    name = _("Console OTP")
    weight = 50

