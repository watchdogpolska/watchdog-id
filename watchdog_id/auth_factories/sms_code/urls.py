# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PhoneNumberListView.as_view(), name="list"),
    url(r'^$', views.PhoneNumberListView.as_view(), name="settings"),
    url(r'^authenticate$', views.SelectPhoneView.as_view(), name="index"),
    url(r'^authenticate-(?P<phone_id>\d+)$', views.ValidateCodeView.as_view(), name="index"),
    url(r'^~create$', views.PhoneNumberCreateView.as_view(), name="create"),
    url(r'^phone-(?P<pk>\d+)$', views.PhoneNumberDetailView.as_view(), name="details"),
    url(r'^phone-(?P<pk>\d+)/~update$', views.PhoneNumberUpdateView.as_view(), name="update"),
    url(r'^phone-(?P<pk>\d+)/~delete$', views.PhoneNumberDeleteView.as_view(), name="delete"),
]
