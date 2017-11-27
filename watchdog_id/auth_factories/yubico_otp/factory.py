from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.factory import BaseFactory


class YubicoOtpFactory(BaseFactory):
    id = 'yubico_otp'
    urlpatterns = 'watchdog_id.auth_factories.yubico_otp.urls'
    name = _("Yubico OTP")
    weight = 50

    def is_available(self, user):
        return True

    def is_enabled(self, user):
        return True
