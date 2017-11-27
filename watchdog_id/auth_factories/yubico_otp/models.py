# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class YubicoOTPDeviceQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class YubicoOTPDevice(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    device_id = models.CharField(max_length=12, verbose_name=_("Device ID"))
    device_name = models.CharField(max_length=25,
                                   default=_("Yubico Token"),
                                   verbose_name=_("Device name"),
                                   help_text=_("Affordable user name token"))
    last_used = models.DateTimeField(null=True, blank=True, verbose_name=_("Last used"),
                                     help_text=_("Time of last use of the token"))
    objects = YubicoOTPDeviceQuerySet.as_manager()

    class Meta:
        verbose_name = _("Yubico OTP Device")
        verbose_name_plural = _("Yubico OTP Devices")
        ordering = ['created', ]

    def __str__(self):
        return "YubicoOTPDevice [{}]".format(self.device_id)
