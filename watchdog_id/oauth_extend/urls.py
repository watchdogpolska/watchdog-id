from __future__ import absolute_import
from django.conf.urls import url

from oauth2_provider import views as views_oauth2

from . import views
urlpatterns = [
    url(r'^authorize/$',
        views_oauth2.AuthorizationView.as_view(),
        name="authorize"),
    url(r'^token/$',
        views_oauth2.TokenView.as_view(),
        name="token"),
    url(r'^revoke_token/$',
        views_oauth2.RevokeTokenView.as_view(),
        name="revoke-token"),
]

# Application management views
urlpatterns += [
    url(r'^applications/$',
        views_oauth2.ApplicationList.as_view(), name="list"),
    url(r'^applications/register/$',
        views.ProtectedApplicationRegistration.as_view(),
        name="register"),
    url(r'^applications/(?P<pk>\d+)/$',
        views_oauth2.ApplicationDetail.as_view(),
        name="detail"),
    url(r'^applications/(?P<pk>\d+)/delete/$',
        views_oauth2.ApplicationDelete.as_view(),
        name="delete"),
    url(r'^applications/(?P<pk>\d+)/update/$',
        views_oauth2.ApplicationUpdate.as_view(),
        name="update"),
]

urlpatterns += [
    url(r'^authorized_tokens/$',
        views_oauth2.AuthorizedTokensListView.as_view(),
        name="authorized-token-list"),
    url(r'^authorized_tokens/(?P<pk>\d+)/delete/$',
        views_oauth2.AuthorizedTokenDeleteView.as_view(),
        name="authorized-token-delete"),
]
