import datetime

from django.urls import reverse

from watchdog_id.auth_oidc.utils import unix


class IdentityToken(object):
    def __init__(self, user):
        self.user = user

    def get_claim(self, request, client, exp_delta=None):
        exp_delta = exp_delta or datetime.timedelta(seconds=300)
        claim = {
            "iss": request.build_absolute_uri(reverse('home')),
            "aud": client.pk,
            "iat": unix(datetime.datetime.now()),
            "exp": unix(datetime.datetime.now() + exp_delta),
        }
        claim.update(self.get_userinfo())
        return claim

    def get_userinfo(self):
        return {"sub": self.user.username,
                "name": self.user.name,
                "email": self.user.email,
                "email_verified": hasattr(self.user, 'activation')}
