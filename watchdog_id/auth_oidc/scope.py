
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_oidc.registers import scope_registry


class BaseScope(object):
    description = _("Not provided.")


@scope_registry.register('openid')
class OpenIDScope(BaseScope):
    description = _("Basic identification details (first name, last name, e-mail address).")
