from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from . consumers import NotificationConsumer


websocket_urlpatterns = [
    path("", NotificationConsumer.as_asgi()),
]
