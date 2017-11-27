# -*- coding: utf-8 -*-
import pyotp as pyotp
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from model_utils.models import TimeStampedModel


class OTPPasswordQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class OTPPassword(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    device_name = models.CharField(max_length=25, help_text=_("Device name"))
    last_used = models.DateTimeField(null=True, blank=True, help_text=_("Time of last use of the token"))
    shared_secret = models.CharField(max_length=16, help_text=_("base32 secret"))
    objects = OTPPasswordQuerySet.as_manager()

    class Meta:
        verbose_name = _("OTP Password")
        verbose_name_plural = _("OTP Passwords")
        ordering = ['created', ]

    def __str__(self):
        return "Token [{}]".format(self.device_name)
