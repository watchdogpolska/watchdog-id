from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.factory import BaseFactory


class RecoveryMailFactory(BaseFactory):
    id = 'recovery_mail'
    urlpatterns = 'watchdog_id.auth_factories.recovery_mail.urls'
    name = _("Recovering access via e-mail")
    first_class = True
    weight = 150

    def is_available(self, user):
        return True

    def is_enabled(self, user):
        return True

    def get_settings_url(self):
        return None
