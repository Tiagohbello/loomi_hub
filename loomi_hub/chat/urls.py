from django.urls import path, include
from rest_framework.routers import DefaultRouter

from loomi_hub.chat.apis.viewsets import ConversationViewSet, MessageViewSet

drf_router = DefaultRouter()

drf_router.register(r"convesations", ConversationViewSet, basename="conversations")
drf_router.register(r"messages", MessageViewSet, basename="messages")


urlpatterns = [
    path("", include(drf_router.urls)),
]
