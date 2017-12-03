# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    www = models.URLField(_("Website"), blank=True, max_length=255)
    telephone = models.CharField(_("Telephone"), blank=True, max_length=25)

    def __str__(self):
        return self.name or self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
