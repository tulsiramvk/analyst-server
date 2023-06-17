from channels.auth import AuthMiddlewareStack
import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

django_asgi_app = get_asgi_application()

from ws import routing  # noqa isort:skip

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa isort:skip
# from ws.token_authentication import TokenAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
        )
    }
)
