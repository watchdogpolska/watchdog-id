from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from watchdog_id.auth_factories.models import Factor


class SharedSecretFactor(models.Model):
    factor = models.ForeignKey(to=Factor,
                               verbose_name=_("Factor"))
    secret_key = models.CharField(verbose_name=_("Secret key"),
                                  max_length=100)
