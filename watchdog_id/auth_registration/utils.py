from datetime import timedelta

from django.core.signing import TimestampSigner

from watchdog_id.users.models import User


class ActivationCodeGenerator(object):
    UNSAFE_CHAR = '+/=:'
    SAFE_CHAR = '~_-.'

    def __init__(self, signer=None, max_age=None):
        print(self.__class__.__name__)
        self.signer = signer or TimestampSigner(salt=self.__class__.__name__)
        self.max_age = max_age or timedelta(days=7)

    def encode(self, user):
        return self.signer.sign(user.pk).translate(
            {ord(s): d for s, d in zip(self.UNSAFE_CHAR, self.SAFE_CHAR)}
        )

    def decode(self, ciphertext):
        user_pk = self.signer.unsign(ciphertext.translate(
            {ord(s): d for s, d in zip(self.SAFE_CHAR, self.UNSAFE_CHAR)}
        ))
        return User.objects.get(pk=user_pk)
