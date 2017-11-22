from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.config import BaseConfig
from watchdog_id.auth_factories.password import views


class TOTPFactory(BaseConfig):
    id = 'totp'
    urlpatterns = 'watchdog_id.auth_factories.totp.urls'
    name = _("TOTP token")
    weight = 100

    def is_enabled(self, user):
        return user.otppassword_set.all().exists()
