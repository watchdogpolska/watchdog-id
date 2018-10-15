from datetime import timedelta

from django.core.signing import TimestampSigner

from watchdog_id.users.models import User


class ActivationCodeGenerator(object):
    MAP = {'+': '~',
           '/': '_'}

    def __init__(self, signer=None, max_age=None):
        self.signer = signer or TimestampSigner(salt=self.__class__.__name__)
        self.max_age = max_age or timedelta(days=7)

    def encode(self, user):
        cipher = self.signer.sign(user.pk)
        ciphertext = cipher.translate(
            {ord(s): d for s, d in zip(self.MAP.keys(), self.MAP.values())}
        )
        return ciphertext

    def decode(self, ciphertext):
        cipher = ciphertext.translate(
            {ord(s): d for s, d in zip(self.MAP.keys(), self.MAP.values())}
        )
        user_pk = self.signer.unsign(cipher)
        return User.objects.get(pk=user_pk)
