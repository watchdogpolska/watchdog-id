from __future__ import unicode_literals

from django.db import models

from watchdog_id.auth_factories import Registry
from watchdog_id.users.models import User


class Factor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=10,
                              choices=Registry.keys())

    @property
    def config(self):
        return Registry[self.method]

    def get_url(self):
        return self.config.get_authentication_url()

    def get_name(self):
        return self.config.name
