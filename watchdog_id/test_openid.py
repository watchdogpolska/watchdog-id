from urllib.parse import urlparse, parse_qsl

import openid_connect

import warnings
import requests
import contextlib

import sys

try:
    from functools import partialmethod
except ImportError:
    # Python 2 fallback: https://gist.github.com/carymrobbins/8940382
    from functools import partial

    class partialmethod(partial):
        def __get__(self, instance, owner):
            if instance is None:
                return self

            return partial(self.func, instance, *(self.args or ()), **(self.keywords or {}))


@contextlib.contextmanager
def no_ssl_verification():
    old_request = requests.Session.request
    requests.Session.request = partialmethod(old_request, verify=False)

    warnings.filterwarnings('ignore', 'Unverified HTTPS request')
    yield
    warnings.resetwarnings()

    requests.Session.request = old_request


def get_code():
    if len(sys.argv) < 2:
        url = input("Copy here redirect_uri: ")
        url_parts = list(urlparse(url))
        url_query = dict(parse_qsl(url_parts[4]))
        return url_query['code']
    return sys.argv[1]


with no_ssl_verification():
    import openid_connect
    client = openid_connect.connect_url('https://1:A@localhost:8000/')
    print("Issuer: ", client.issuer)
    print("JWKS", client.keys)
    print(client.authorize(redirect_uri="http://onet.pl/", state="A"))
    code = get_code()
    print("Code: ", code)
    print(client.request_token(redirect_uri="http://onet.pl/", code=code))
