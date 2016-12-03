# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<slug>[-\w]+)/',
        views.PostDetailView.as_view(), name="details"),
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/',
        views.PostMonthArchiveView.as_view(), name="list"),
    url(r'^$', views.PostArchiveIndexView.as_view(), name="list"),
]
