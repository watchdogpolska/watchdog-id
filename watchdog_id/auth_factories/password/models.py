from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
from autoslug.fields import AutoSlugField


class PasswordSettingsQuerySet(models.QuerySet):
    pass


class PasswordSettings(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    status = models.BooleanField(default=True)
    objects = PasswordSettingsQuerySet.as_manager()

    class Meta:
        verbose_name = _("Password Setting")
        verbose_name_plural = _("Password Settings")
        ordering = ['created', ]

    def __str__(self):
        return "PasswordSettings of #{} [status={}]".format(self.user_id, self.status)
