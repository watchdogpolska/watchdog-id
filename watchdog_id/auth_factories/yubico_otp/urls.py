from django.conf.urls import url

from watchdog_id.auth_factories.yubico_otp import views

urlpatterns = [
    url(r'^$', views.AuthenticationView.as_view(), name="index"),
    url(r'^settings$', views.YubicoOTPDeviceListView.as_view(), name="settings"),
    url(r'^settings$', views.YubicoOTPDeviceListView.as_view(), name="list"),
    url(r'^~create$', views.YubicoOTPDeviceCreateView.as_view(), name="create"),
    # url(r'^token-(?P<pk>\d+)/~update$', views.Yubico.as_view(), name="update"),
    url(r'^token-(?P<pk>[\d]+)/~delete$', views.YubicoOTPDeviceDeleteView.as_view(), name="delete"),
]
