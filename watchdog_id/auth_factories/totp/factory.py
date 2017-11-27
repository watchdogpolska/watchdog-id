from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.factory import BaseFactory


class TOTPFactory(BaseFactory):
    id = 'totp'
    urlpatterns = 'watchdog_id.auth_factories.totp.urls'
    name = _("TOTP token")
    weight = 100

    def is_enabled(self, user):
        return user.otppassword_set.all().exists()
