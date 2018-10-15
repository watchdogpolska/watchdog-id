import json

import jwcrypto
import jwcrypto.jwk
from datetime import datetime
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from six.moves.urllib.parse import urlparse

from watchdog_id.auth_oidc.registers import scope_registry
from watchdog_id.auth_oidc.settings import OIDC_KEY_TYPE, OIDC_ACCESS_TOKEN_LIFETIME

jwk_type_supported = iter(list(jwcrypto.jwk.JWKTypesRegistry.items()))


class ClientAuthenticationQuerySet(models.QuerySet):
    pass


class Application(TimeStampedModel):
    PROFILES = Choices(('web', _('web application')),
                       ('user-agent', _('user-agent-based application')),
                       ('native', _('native application')))
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # See RFC 6749 section 2.1
    profile = models.CharField(choices=PROFILES, default=PROFILES.web, max_length=20)

    client_secret = models.CharField(verbose_name=_("Client secret"), max_length=200)

    redirect_uri_list = models.TextField(verbose_name=_("Redirect URI list"),
                                         help_text=_("List of allowed addresses. One address per line. "
                                                     "The domain address and path are compared."
                                                     "It is implied that the addresses are HTTPS."))
    objects = ClientAuthenticationQuerySet.as_manager()

    # See RFC 6749 section 2.3.1
    @property
    def client_id(self):
        return self.id

    def check_redirect_uri(self, uri):
        return True
        uri_parsed = urlparse(uri)
        if uri_parsed.scheme != "https":
            return False
        for valid_uri in self.redirect_uri_list.strip().split("\n"):
            valid_uri_parsed = urlparse(valid_uri)
            if valid_uri_parsed.netloc != uri_parsed.netloc:
                continue
            if valid_uri_parsed.path != uri_parsed.path:
                continue
            return True
        return False

    @property
    def confidentiality_credentials(self):  # See RFC 6749 section 2.1
        if self.profile in ['web', 'user-agent']:
            return True
        return False

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        ordering = ['created', ]

    def __str__(self):
        return self.name


class GrantQuerySet(models.QuerySet):
    pass


class Grant(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    scope = models.CharField(verbose_name=_("Scope"),
                             max_length=50,
                             choices=scope_registry.keys())
    objects = GrantQuerySet.as_manager()

    class Meta:
        verbose_name = _("Grant")
        verbose_name_plural = _("Grants")
        ordering = ['created', ]


class TokenQuerySet(models.QuerySet):
    def valid_at(self, time=None):
        time = time or datetime.now()
        return self.filter(created_gte=time - OIDC_ACCESS_TOKEN_LIFETIME)


@python_2_unicode_compatible
class BearerToken(TimeStampedModel):
    """
        Access Token
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret = models.CharField(max_length=100)
    code = models.ForeignKey('Code', null=True, blank=True)
    objects = TokenQuerySet.as_manager()

    def __str__(self):
        return "Token[created={}, user_id={}]".format(self.created, self.user_id)

    @staticmethod
    def get_random_secret():
        return get_random_string(100)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")


@python_2_unicode_compatible
class RefreshToken(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret = models.CharField(max_length=100)
    code = models.ForeignKey('Code', null=True, blank=True)

    @staticmethod
    def get_random_secret():
        return get_random_string(100)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")


class CodeQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Code(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    redirect_uri = models.CharField(max_length=200)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    secret = models.CharField(max_length=100)
    used = models.BooleanField(default=False, help_text=_("Determines if the code has been used before."))

    @staticmethod
    def get_random_secret():
        return get_random_string(100)

    class Meta:
        verbose_name = _("Code")
        verbose_name_plural = _("Codes")
        ordering = ['created', ]


class JWKeyQuerySet(models.QuerySet):
    # See latchset/jwcrypto#104 and latchset/jwcrypto#28
    def get_or_generate(self, site):
        try:
            key = self.filter(site=site, kty=OIDC_KEY_TYPE).get()
            jwk = jwcrypto.jwk.JWK(**json.loads(key.export), kid=key.id)
        except JWKey.DoesNotExist:
            jwk = jwcrypto.jwk.JWK.generate(kty=OIDC_KEY_TYPE)
            JWKey.objects.create(site=site,
                                 kty=OIDC_KEY_TYPE,
                                 export=jwk.export())
        return jwk

    def get_all_keys(self, site):
        return [jwcrypto.jwk.JWK(**json.loads(key.export))
                for key in self.filter(site=site, kty=OIDC_KEY_TYPE).all()]

    def get_sign_keys(self, site):
        data = []
        for key in self.get_all_keys(site):
            key = jwcrypto.jwk.JWK(**json.loads(key.export()), use='sig')
            data.append(key)
        return data


@python_2_unicode_compatible
class JWKey(TimeStampedModel):
    site = models.ForeignKey(to=Site, verbose_name=_("Site"))
    kty = models.CharField(verbose_name=_("Key Types"), max_length=5, choices=jwk_type_supported)
    export = models.TextField(verbose_name=_("Export of key"))
    objects = JWKeyQuerySet.as_manager()

    class Meta:
        verbose_name = _("Json Web Key")
        verbose_name_plural = _("Json Web Keys")
        ordering = ['created', ]
        index_together = [('site', 'kty'), ]
        unique_together = [('site', 'kty'), ]
