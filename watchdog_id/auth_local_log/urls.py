# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.LogEntryListView.as_view(), name="list"),
    url(r'^$', views.LogEntryListView.as_view(), name="index"),
    url(r'^entry-(?P<pk>\d+)$', views.LogEntryDetailView.as_view(), name="details"),
]
