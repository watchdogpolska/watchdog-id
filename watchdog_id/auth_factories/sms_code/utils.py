from twilio.rest import Client

from watchdog_id.auth_factories.sms_code.settings import AUTH_KEY, AUTH_SECRET


def get_client():
    return Client(AUTH_KEY, AUTH_SECRET)
