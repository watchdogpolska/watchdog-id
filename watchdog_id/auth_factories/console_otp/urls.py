from django.conf.urls import url

from watchdog_id.auth_factories.console_otp import views

urlpatterns = [
    url(r'^$', views.AuthenticationView.as_view(), name="index"),

]
