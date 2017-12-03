# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class U2FTokenQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class U2FToken(TimeStampedModel):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='u2f_tokens')
    device_name = models.CharField(max_length=15,
                                   verbose_name=_("Device name"),
                                   default=_("Standard token"))
    device_data = models.TextField(verbose_name=_("Authentication data"))
    last_used = models.DateTimeField(null=True, blank=True,
                                     verbose_name=_("Last used"),
                                     help_text=_("Time of last use of the token"))
    objects = U2FTokenQuerySet.as_manager()

    class Meta:
        verbose_name = _("U2F token")
        verbose_name_plural = _("U2F tokens")
        ordering = ['created', ]

    def get_absolute_url(self):
        return reverse('auth_factories:u2ftoken:details', args=[self.pk])

    def __str__(self):
        return self.device_name
