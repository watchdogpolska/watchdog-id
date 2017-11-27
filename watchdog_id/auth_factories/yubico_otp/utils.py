from yubico_client import Yubico

from watchdog_id.auth_factories.yubico_otp.settings import YUBICO_AUTH_CLIENT_ID, YUBICO_AUTH_SECRET_KEY


def get_client():
    return Yubico(YUBICO_AUTH_CLIENT_ID, YUBICO_AUTH_SECRET_KEY)
