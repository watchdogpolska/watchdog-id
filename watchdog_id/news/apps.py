from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NewsConfig(AppConfig):
    name = 'watchdog_id.news'
    verbose_name = _("News")

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
