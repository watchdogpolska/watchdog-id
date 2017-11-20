from django.conf.urls import url

from watchdog_id.auth_factories.password import views

urlpatterns = [
    url(r'^$', views.PasswordLoginView.as_view(), name="index"),

]
