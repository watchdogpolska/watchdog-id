from abc import abstractmethod, ABCMeta

from django.shortcuts import redirect

from watchdog_id.auth_oidc.registers import response_mode_registry
from watchdog_id.auth_oidc.utils import url_parametized


class AbstractResponseMode(object, metaclass=ABCMeta):
    @abstractmethod
    def get_response(self, url, params):
        pass


@response_mode_registry.register('fragment')
class FragmentMode(AbstractResponseMode):
    def get_response(self, url, params):
        return redirect(url_parametized(url, params_fragment=params))


@response_mode_registry.register('query')
class QueryMode(AbstractResponseMode):
    def get_response(self, url, params):
        return redirect(url_parametized(url, params_qs=params))
