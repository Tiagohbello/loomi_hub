from django.urls import path
from .consumers import ChatConsumer

chat_websocket_urlpatterns = [
    path('ws/chat/<uuid:id>/', ChatConsumer.as_asgi()),
]