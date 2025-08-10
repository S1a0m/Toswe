# asgi.py

import os
import django

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import toswe.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toswe.settings')
django.setup()

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(toswe.routing.websocket_urlpatterns)
    ),
})
