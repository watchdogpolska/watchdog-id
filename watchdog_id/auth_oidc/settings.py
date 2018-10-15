import datetime

from django.conf import settings

OIDC_KEY_TYPE = getattr(settings, 'OIDC_KEY_TYPE', 'RSA')

OIDC_ACCESS_TOKEN_LIFETIME = getattr(settings,
                                     'OIDC_ACCESS_TOKEN_LIFETIME',
                                     datetime.timedelta(hours=1))

OIDC_REFRESH_TOKEN_LIFETIME = getattr(settings,
                                      'OIDC_REFRESH_TOKEN_LIFETIME',
                                      datetime.timedelta(hours=6))

# ACCESS_TOKEN_LIFETIME = OIDC_ACCESS_TOKEN_LIFETIME.total_seconds()
