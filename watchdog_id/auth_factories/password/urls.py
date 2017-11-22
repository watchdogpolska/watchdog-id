from django.conf.urls import url

from watchdog_id.auth_factories.password import views

urlpatterns = [
    url(r'^$', views.AuthenticationView.as_view(), name="index"),
    url(r'^settings$', views.SettingsView.as_view(), name="settings"),
]
