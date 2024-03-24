"""
ASGI config for loomi_hub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from loomi_hub.chat import routing
from loomi_hub.middlewares import TokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loomi_hub.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns))
        ),
    }
)
