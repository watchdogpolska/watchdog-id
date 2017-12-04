from django.conf import settings

AUTH_KEY = getattr(settings, 'TWILLO_AUTH_KEY', None)

AUTH_SECRET = getattr(settings, 'TWILLO_AUTH_SECRET', None)

FROM_NUMBER = getattr(settings, 'TWILLO_FROM_NUMBER', None)

MAX_BID = getattr(settings, 'TWILLO_MAX_BID', 0.5)
