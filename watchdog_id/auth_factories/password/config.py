from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.config import BaseConfig
from watchdog_id.auth_factories.password import views


class PasswordConfig(BaseConfig):
    id = 'password'
    urlpatterns = 'watchdog_id.auth_factories.password.urls'
    name = _("Password")
