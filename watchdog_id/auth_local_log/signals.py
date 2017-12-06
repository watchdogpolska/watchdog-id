# coding=utf-8
import django.dispatch
from django.dispatch import receiver

from watchdog_id.auth_factories.signals import user_authenticated, factory_authenticated, user_identified, user_logout
from watchdog_id.auth_local_log.models import LogEntry

common = ["user", "session_id", "request_ip"]


@receiver(user_identified)
def user_identified_handler(sender, user, request_ip, session_id=None, **kwargs):
    LogEntry.objects.create(event_type="user_identified",
                            user=user,
                            session_key=session_id or '',
                            request_ip=request_ip)


@receiver(factory_authenticated)
def factory_authenticated_handler(sender, user, session_id, request_ip, factory, extra, **kwargs):
    LogEntry.objects.create(event_type="factory_authenticated",
                            user=user,
                            session_key=session_id,
                            request_ip=request_ip,
                            extra_data={'factory': factory.id, 'extra': extra})


@receiver(user_authenticated)
def user_authenticated_handler(sender, user, session_id, request_ip, **kwargs):
    LogEntry.objects.create(event_type="user_authenticated",
                            user=user,
                            session_key=session_id,
                            request_ip=request_ip)


@receiver(user_logout)
def user_logout_handler(sender, user, session_id, request_ip, **kwargs):
    LogEntry.objects.create(event_type="user_logout",
                            user=user,
                            session_key=session_id,
                            request_ip=request_ip)
