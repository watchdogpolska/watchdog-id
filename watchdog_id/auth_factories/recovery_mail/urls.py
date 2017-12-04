from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.EmailSendView.as_view(), name="index"),
    url(r'^confirmation-(?P<code>\d+)-(?P<request_id>\d+)', views.EmailConfirmationView.as_view(), name="confirmation"),
]
