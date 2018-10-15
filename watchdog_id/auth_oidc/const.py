# coding=utf-8
from enum import Enum


class AuthorizationFlow(Enum):
    CODE = 'code'
    IMPLICIT = 'implicit'
    HYBRID = 'hybrid'


class ResponseTypes(object):
    MAP = {'code': (AuthorizationFlow.CODE,
                    "query"),

           # TODO: Response types
           # 'id_token': (AuthorizationFlow.IMPLICIT,
           #              "query"),
           # 'id_token token': (AuthorizationFlow.IMPLICIT,
           #                    "fragment"),
           # 'code id_token': (AuthorizationFlow.HYBRID,
           #                   "fragment"),
           # 'code token': (AuthorizationFlow.HYBRID,
           #                "fragment"),
           # 'code id_token token': (AuthorizationFlow.HYBRID,
           #                         "fragment")
           }

    @classmethod
    def get_authorization_flow(cls, response_type):
        return cls.MAP[response_type][0]

    @classmethod
    def get_default_response_mode(cls, response_type):
        return cls.MAP[response_type][1]

    @classmethod
    def get_response_types(cls):
        return cls.MAP.keys()
