from django.conf import settings

YUBICO_AUTH_CLIENT_ID = getattr(settings, 'YUBICO_AUTH_CLIENT_ID')

YUBICO_AUTH_SECRET_KEY = getattr(settings, 'YUBICO_AUTH_SECRET_KEY')
