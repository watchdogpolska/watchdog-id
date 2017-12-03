# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class OTPPasswordQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class OTPPassword(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=25, verbose_name=_("Device name"))
    last_used = models.DateTimeField(null=True, blank=True, verbose_name=_("Last used"),
                                     help_text=_("Time of last use of the token"))
    shared_secret = models.CharField(max_length=16, verbose_name=_("base32 secret"))
    objects = OTPPasswordQuerySet.as_manager()

    class Meta:
        verbose_name = _("OTP Password")
        verbose_name_plural = _("OTP Passwords")
        ordering = ['created', ]

    def __str__(self):
        return "Token [{}]".format(self.device_name)
