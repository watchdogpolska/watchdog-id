# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from . import views, Registry

urlpatterns = [
   url(r'^$', views.LoginFormView.as_view(), name="login"),
   url(r'^logout$', views.LogoutActionView.as_view(), name="logout"),
   url(r'^list$', views.FactorListView.as_view(), name="list"),
]


for id, cfg in Registry.items():
    urlpatterns.append(url(id + '/', include(cfg.urlpatterns, namespace=id)))
