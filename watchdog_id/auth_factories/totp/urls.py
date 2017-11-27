from django.conf.urls import url

from watchdog_id.auth_factories.totp import views

urlpatterns = [
    url(r'^$', views.AuthenticationView.as_view(), name="index"),
    url(r'^settings$', views.OTPPasswordListView.as_view(), name="settings"),
    url(r'^settings$', views.OTPPasswordListView.as_view(), name="list"),
    url(r'^~create$', views.OTPPasswordCreateView.as_view(), name="create"),
    url(r'^token-(?P<pk>\d+)/~update$', views.OTPPasswordUpdateView.as_view(), name="update"),
    url(r'^token-(?P<pk>[\d]+)/~delete$', views.OTPPasswordDeleteView.as_view(), name="delete"),
]
