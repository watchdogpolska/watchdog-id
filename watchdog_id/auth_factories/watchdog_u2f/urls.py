from django.conf.urls import url

from watchdog_id.auth_factories.watchdog_u2f import views

urlpatterns = [
    url(r'^$', views.AuthenticationView.as_view(), name="index"),
    url(r'^settings$', views.U2FTokenListView.as_view(), name="settings"),
    url(r'^settings$', views.U2FTokenListView.as_view(), name="list"),
    url(r'^~create$', views.U2FTokenCreateView.as_view(), name="create"),
    url(r'^token-(?P<pk>\d+)$', views.U2FTokenDetailsView.as_view(), name="details"),
    url(r'^token-(?P<pk>\d+)/~update$', views.U2FTokenUpdateView.as_view(), name="update"),
    url(r'^token-(?P<pk>[\d]+)/~delete$', views.U2FTokenDeleteView.as_view(), name="delete"),
]
