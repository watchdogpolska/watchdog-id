# from django.conf import settings
import base64
import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from jwcrypto import jwt

from watchdog_id.auth_factories.managers import UserAuthenticationManager
from watchdog_id.auth_oidc.const import ResponseTypes
from watchdog_id.auth_oidc.id_token import IdentityToken
from watchdog_id.auth_oidc.models import Application, Code, BearerToken, RefreshToken, JWKey
from watchdog_id.auth_oidc.registers import response_mode_registry
from watchdog_id.auth_oidc.settings import OIDC_ACCESS_TOKEN_LIFETIME

logger = logging.getLogger(__name__)


class DiscoveryView(View):
    def dispatch(self, request, *args, **kwargs):
        return JsonResponse(self.get_discovery_info(request))

    def get_discovery_info(self, request):
        info = {}

        info["issuer"] = request.build_absolute_uri(reverse('home'))
        info["authorization_endpoint"] = request.build_absolute_uri(reverse('auth_oidc:authorization'))
        info["token_endpoint"] = request.build_absolute_uri(reverse('auth_oidc:token'))
        # info["token_endpoint_auth_methods_supported"] = ["client_secret_basic"]
        info['jwks_uri'] = request.build_absolute_uri(reverse('auth_oidc:jwks'))
        info["userinfo_endpoint"] = request.build_absolute_uri(reverse('auth_oidc:userinfo'))
        info["check_session_iframe"] = request.build_absolute_uri(reverse('auth_oidc:check_session'))
        info["end_session_endpoint"] = request.build_absolute_uri(reverse('auth_oidc:end_session'))
        # info["scopes_supported"] = list(scope_registry.keys())
        info["response_types_supported"] = list(ResponseTypes.get_response_types())
        info['subject_types_supported'] = ['public']
        info["ui_locales_supported"] = [x for x, _ in settings.LANGUAGES]
        return info


class ResponseErrorException(Exception):
    def __init__(self, code, msg=None, uri=None):
        self.code = code
        self.msg = msg
        self.uri = uri

    def as_dict(self, state=None):
        params = {'code': self.code}
        if self.msg:
            params['error_description'] = self.msg
        if state:
            params['state'] = state
        return params


class HttpJsonResponseBadRequest(JsonResponse):
    status_code = 400


class AuthorizationView(AccessMixin, TemplateView):

    def get_template_names(self):
        return ['auth_oidc/consent_{}.html'.format(self.response_display),
                'auth_oidc/consent.html']

    error_messages = {
        # See RFC 6749 4.1.2.1
        "invalid_request": "invalid_request",
        # See OpenID spec
        "interaction_required": "interaction_required",
        "login_required": "login_required",
        "account_selection_required": "account_selection_required",
        "consent_required": "consent_required",
        "invalid_request_uri": "invalid_request_uri",
        "invalid_request_object": "invalid_request_object",
        "request_not_supported": "request_not_supported",
        "request_uri_not_supported": "request_uri_not_supported",
        "registration_not_supported": "registration_not_supported",
        "subject_types_supported": ["public", ]
    }

    def check_oauth_manner(self, request):
        """
        Validate all the OAuth 2.0 parameters according to the OAuth 2.0 specification.
        :param request:
        :return: validation result
        """
        if not request.GET.get('client_id') or not request.GET.get('redirect_uri'):
            logger.error("Missing params 'client_id' or 'redirect_uri'")
            return False
        self.client_id = request.GET['client_id']
        self.redirect_uri = request.GET['redirect_uri']
        try:
            self.client = Application.objects.get(id=self.client_id)
        except (Application.DoesNotExist, ValueError):
            logger.error("Invalid 'client_id'")
            return False

        if not self.client.check_redirect_uri(request.GET['redirect_uri']):
            logger.error("Invalid 'redirect_uri'")
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        self.user_manager = UserAuthenticationManager(request.session)

        if not self.check_oauth_manner(request):
            messages.error(request, self.error_messages["invalid_request"])
            return redirect('home')

        try:
            self.verify_required_parameters(request)
            self.verify_response_type(request)
            self.verify_response_mode(request)
            self.verify_scope_parameter(request)
            self.verify_prompt_parameter(request)
            self.verify_display(request)
            self.verify_prompt_parameter(request)
            if not self.user_manager.get_user().is_authenticated:
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
        except ResponseErrorException as e:
            params = e.as_dict(state=request.GET.get('state', None))
            return self.get_response(request.GET['redirect_uri'], params)

    def verify_required_parameters(self, request):
        """
        Verify that all the REQUIRED parameters are present and their usage conforms to this specification.
        """
        if 'scope' not in request.GET:
            raise ResponseErrorException(code='invalid_request',
                                         msg="Missing 'scope' parameter.")
        self.scope = request.GET['scope']
        if 'response_type' not in request.GET:
            raise ResponseErrorException(code='invalid_request',
                                         msg="Missing 'response_type' parameter.")
        self.response_type = request.GET['response_type']

    def verify_scope_parameter(self, request):
        """
        # Verify that a scope parameter is present and contains the openid scope value.
        """
        self.scopes = request.GET['scope'].strip().split(" ")
        if "openid" not in self.scopes:
            raise ResponseErrorException(code='invalid_request',
                                         msg="No 'openid' scope value is present.")

    def verify_display(self, request):
        self.response_display = request.GET.get('display', 'page')
        allowed = ['page', 'popup', 'touch', 'wap']
        if self.response_display not in allowed:
            raise ResponseErrorException(code='invalid_request',
                                         msg="Invalid 'display' parameter. Must be one of {}.".format(allowed))

    def verify_prompt_parameter(self, request):
        if 'prompt' not in request.GET:
            self.prompt = None
            self.prompt_list = None
            return
        self.prompt = request.GET['prompt']
        self.prompt_list = self.prompt.split(' ')
        allowed = ['none', 'login', 'consent', 'select_account']
        for value in self.prompt_list:
            if value not in allowed:
                raise ResponseErrorException(code='invalid_request',
                                             msg="Invalid 'prompt' parameter. May contains "
                                                 "only {}.".format(allowed))
        if self.user_manager.get_user().is_anonymous and self.prompt == 'none':
            raise ResponseErrorException(code='login_required')

    def post(self, request, *args, **kwargs):
        code = Code.objects.create(redirect_uri=self.redirect_uri,
                                   application=self.client,
                                   user=request.user,
                                   secret=get_random_string(100))
        params = {'code': code.secret}
        if 'state' in request.GET:
            params['state'] = request.GET['state']
        return self.get_response(self.redirect_uri, params)

    def verify_response_type(self, request):
        self.response_type = request.GET['response_type']
        allowed = ResponseTypes.get_response_types()
        if self.response_type not in allowed:
            raise ResponseErrorException(code='invalid_request',
                                         msg="Invalid 'response_type' parameter. May contains "
                                             "only {}.".format(allowed))

    def verify_response_mode(self, request):
        self.response_mode = request.GET.get('response_mode',
                                             ResponseTypes.get_default_response_mode(self.response_type))
        allowed = list(response_mode_registry.keys())
        if self.response_mode not in allowed:
            raise ResponseErrorException(code='invalid_request',
                                         msg="Invalid 'response_mode' parameter. May contains "
                                             "only {}.".format(allowed))

    def get_response(self, url, params):
        response_mode = response_mode_registry[self.response_mode]
        return response_mode.get_response(url, params)


class ErrorResponseMixin(View):

    def dispatch(self, request, *args, **kwargs):
        try:
            super(ErrorResponseMixin, self).dispatch(request, *args, **kwargs)
        except ResponseErrorException as e:
            return HttpJsonResponseBadRequest(data=e.as_dict())


LINK_RFC_ERROR_CODE = 'https://tools.ietf.org/html/rfc6749#section-4.1.3'
LINK_OPENID_VALIDATION_TOKEN = 'http://openid.net/specs/openid-connect-core-1_0.html#TokenRequestValidation'


class TokenView(ErrorResponseMixin, View):
    hard_required_parameters = ['grant_type', 'code']

    def validate_parameters(self, params=None):
        params = params or {}
        for param in self.hard_required_parameters:
            if param not in self.request.POST:
                raise ResponseErrorException(code='invalid_request',
                                             msg="Missing '{}' parameter. It is hard required.".format(param),
                                             uri=LINK_RFC_ERROR_CODE)
            params[param] = self.request.POST[param]
        if params['grant_type'] != 'authorization_code':
            raise ResponseErrorException(code='invalid_request',
                                         msg="Invalid value of 'grant_type' parameter.",
                                         uri=LINK_RFC_ERROR_CODE)
        try:
            self.code = Code.objects.get(secret=params['code'], application=self.client)
        except Code.DoesNotExist:
            raise ResponseErrorException(code='invalid_request',
                                         msg="Invalid value of 'grant_type' parameter.",
                                         uri=LINK_RFC_ERROR_CODE)
        if self.code.redirect_uri:
            if 'redirect_uri' not in self.request.POST:
                raise ResponseErrorException(code='invalid_request',
                                             msg="'redirect_uri' parameter was included in the initial "
                                                 "Authorization Request.",
                                             uri=LINK_OPENID_VALIDATION_TOKEN)
            if self.request.POST['redirect_uri'] != self.code.redirect_uri:
                raise ResponseErrorException(code='invalid_request',
                                             msg="'redirect_uri' parameter value is identical to the 'redirect_uri'"
                                                 "parameter value that was included in the initial "
                                                 "Authorization Request'",
                                             uri=LINK_OPENID_VALIDATION_TOKEN)
        if self.code.used:
            raise ResponseErrorException(code='invalid_request',
                                         msg="Authorization Code has been previously used.",
                                         uri=LINK_OPENID_VALIDATION_TOKEN)
        # TODO: Verify that the Authorization Code used was issued in response to an
        # OpenID Connect Authentication Request (so that an ID Token will be returned
        # from the Token Endpoint).
        return params

    def post(self, request, *args, **kwargs):
        self.check_credentials(request)
        params = self.validate_parameters()
        # TODO: Uncomment it: self.code.used = True
        self.code.save()
        access_token = BearerToken.objects.create(user=self.code.user,
                                                  secret=BearerToken.get_random_secret(),
                                                  code=self.code)
        refresh_token = RefreshToken.objects.create(user=self.code.user,
                                                    secret=RefreshToken.get_random_secret())
        response_data = {
            "access_token": access_token.secret,
            "refresh_token": refresh_token.secret,
            "token_type": "Bearer",
            "expires_in": int(OIDC_ACCESS_TOKEN_LIFETIME.total_seconds()),
            "id_token": self.get_id_token(self.code.user)
        }
        return JsonResponse(response_data)

    def get_id_token(self, user):
        claim = IdentityToken(user).get_claim(self.request, self.client)
        key = JWKey.objects.get_or_generate(site=get_current_site(self.request))
        token = jwt.JWT(header={"alg": "RSA-OAEP", 'enc': 'A128CBC-HS256'},
                        claims=claim)
        token.make_encrypted_token(key)
        return token.serialize()

    def check_credentials(self, request):
        self.basic_http_authentication(request)

    def basic_http_authentication(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            raise ResponseErrorException(code='invalid_client',
                                         msg='Unsupported authentication method. '
                                             '"Authorization" request header required.')
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if not (len(auth) == 2 and auth[0].lower() == "basic"):
            raise ResponseErrorException(code='invalid_client',
                                         msg='Unsupported authentication method. '
                                             '"Basic" access authentication supported only')
        uname, passwd = base64.b64decode(auth[1]).decode('ascii').split(':')
        try:
            self.client = Application.objects.get(id=uname)
        except Application.DoesNotExist:
            raise ResponseErrorException(code='invalid_client',
                                         msg='Unknown client.')
        if self.client.confidentiality_credentials and not passwd == self.client.client_secret:
            raise ResponseErrorException(code='invalid_client',
                                         msg='Secret required for confindental client.')

    @classmethod
    def as_view(cls, **initkwargs):
        return csrf_exempt(super().as_view(**initkwargs))
i

class CheckSessionView(View):
    pass


class EndSessionView(View):
    pass


class RegisterView(View):
    pass


class UserInfoView(View):
    pass


class JSONWebKeySetView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data=self.get_json_data())

    def get_json_data(self):
        keys = JWKey.objects.get_sign_keys(site=get_current_site(self.request))
        return {'keys': [json.loads(x.export()) for x in keys]}
