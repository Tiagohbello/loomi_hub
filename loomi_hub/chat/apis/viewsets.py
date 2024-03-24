from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from loomi_hub.chat.apis.filters import ConversationFilter, MessageFilter
from loomi_hub.chat.apis.serializers import ConversationSerializer, MessageSerializer
from loomi_hub.chat.models import Conversation, Message


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = ConversationFilter
    http_method_names = ["get", "post"]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    filterset_class = MessageFilter
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
