from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.config import BaseConfig


class PasswordConfig(BaseConfig):
    id = 'password'
    urlpatterns = 'watchdog_id.auth_factories.password.urls'
    name = _("Password")
    weight = 100

    def is_enabled(self, user):
        if not hasattr(user, 'passwordsettings'):  # Password enabled by default
            return True
        return user.passwordsettings.status
