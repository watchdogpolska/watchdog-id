from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.factory import BaseFactory


class WatchdogU2FFactory(BaseFactory):
    id = 'u2ftoken'
    urlpatterns = 'watchdog_id.auth_factories.watchdog_u2f.urls'
    name = _("U2F token")
    weight = 100

    def is_enabled(self, user):
        return user.u2f_tokens.all().exists()
