from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.factory import BaseFactory


class PasswordFactory(BaseFactory):
    id = 'password'
    urlpatterns = 'watchdog_id.auth_factories.password.urls'
    name = _("Password")
    first_class = True
    weight = 100

    def is_enabled(self, user):
        if not hasattr(user, 'passwordsettings'):  # Password enabled by default
            return True
        return user.passwordsettings.status
