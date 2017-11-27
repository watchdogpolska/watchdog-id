from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.config import BaseConfig


class TOTPFactory(BaseConfig):
    id = 'totp'
    urlpatterns = 'watchdog_id.auth_factories.totp.urls'
    name = _("TOTP token")
    weight = 100

    def is_enabled(self, user):
        return user.otppassword_set.all().exists()
