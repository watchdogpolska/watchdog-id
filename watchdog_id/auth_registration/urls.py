# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.RegistrationView.as_view(), name="index"),
    url(r'^activation-(?P<code>[0-9A-Za-z+~_]+)$', views.ConfirmationView.as_view(), name="confirmation"),
]
