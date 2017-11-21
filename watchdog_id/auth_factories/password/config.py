from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.config import BaseConfig
from watchdog_id.auth_factories.password import views


class PasswordConfig(BaseConfig):
    id = 'password'
    urlpatterns = 'watchdog_id.auth_factories.password.urls'
    name = _("Password")
    weight = 100

    def is_available(self, user):
        return True

    def is_enabled(self, user):
        if not hasattr(user, 'passwordsettings'):  # Password enabled by default
            return True
        return user.passwordsettings.status
