from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.factory import BaseFactory
from watchdog_id.auth_factories.sms_code.settings import FROM_NUMBER, AUTH_SECRET, AUTH_KEY


class SmsCodeFactory(BaseFactory):
    id = 'sms_code'
    urlpatterns = 'watchdog_id.auth_factories.sms_code.urls'
    name = _("SMS code")
    weight = 100

    def is_available(self, user):
        return AUTH_KEY and AUTH_SECRET and FROM_NUMBER

    def is_enabled(self, user):
        return user.phonenumber_set.exists()
