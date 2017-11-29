# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from watchdog_id.auth_factories.watchdog_u2f.models import U2FToken


@admin.register(U2FToken)
class U2FTokenAdmin(admin.ModelAdmin):
    pass
