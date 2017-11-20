from django.conf import settings

MIN_WEIGHT = getattr(settings, 'AUTH_FACTORY_MIN_WEIGHT', 50)
