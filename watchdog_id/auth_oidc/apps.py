from django.apps import AppConfig


class AuthOidcConfig(AppConfig):
    name = 'watchdog_id.auth_oidc'
    # verbose_name = _("OpenID Provider")

    def ready(self):
        from . import response_modes
        from . import scope
