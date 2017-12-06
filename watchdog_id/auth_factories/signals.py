# coding=utf-8
import django.dispatch

common = ["user", "session_id", "request_ip"]

user_identified = django.dispatch.Signal(providing_args=common)

factory_authenticated = django.dispatch.Signal(providing_args=common + ["factory", "extra"])

user_authenticated = django.dispatch.Signal(providing_args=common)

user_logout = django.dispatch.Signal(providing_args=common)
