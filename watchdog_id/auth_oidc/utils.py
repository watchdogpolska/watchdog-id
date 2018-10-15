import random
import string
import warnings

from six.moves.urllib.parse import urlparse, urlencode, urlunparse, parse_qsl


def url_parametized(url, params_qs=None, params_fragment=None):
    url_parts = list(urlparse(url))

    url_query = dict(parse_qsl(url_parts[4]))
    url_query.update(params_qs or {})
    url_parts[4] = urlencode(url_query)
    url_parts[5] = urlencode(params_fragment or {})
    return urlunparse(url_parts)


def secure_string(length):
    warnings.warn(
        "The watchdog_id.atuh_oidc.utils.secure_string is deprecated in "
        "favor of django.utils.crypto.get_random_string.",
        DeprecationWarning
    )
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(length))


def unix(time):
    return int(time.strftime("%s"))
