# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^authentication$', views.AuthorizationView.as_view(), name="authorization"),
    url(r'^token$', views.TokenView.as_view(), name="token"),
    url(r'^check-session', views.CheckSessionView.as_view(), name="check_session"),
    url(r'^end-session', views.EndSessionView.as_view(), name="end_session"),
    url(r'^register', views.RegisterView.as_view(), name="register"),
    url(r'^discovery', views.DiscoveryView.as_view(), name="discovery"),
    url(r'^discovery', views.UserInfoView.as_view(), name="userinfo"),
    url(r'^jwks', views.JSONWebKeySetView.as_view(), name='jwks'),
]
