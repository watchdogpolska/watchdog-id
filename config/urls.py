# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from django.views.generic import TemplateView
# from rest_framework import routers
# from watchdog_id.users.viewsets import GroupViewSet, UserViewSet


# Routers provide an easy way of automatically determining the URL conf
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^auth/', include(('watchdog_id.auth_factories.urls', 'auth_factories'))),
    url(r'^auth/logs/', include(('watchdog_id.auth_local_log.urls', 'auth_local_log'))),
    url(r'^registration/', include(('watchdog_id.auth_registration.urls', 'auth_registration'))),
    url(r'^users/', include(('watchdog_id.users.urls', 'users'))),
    # url(r'^api/', include(router.urls)),
    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
