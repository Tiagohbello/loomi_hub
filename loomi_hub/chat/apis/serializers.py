from rest_framework import serializers

from loomi_hub.chat.models import Conversation, ConversationParticipant, Message
from loomi_hub.user.apis.serializers import UserSerializer


class ConversationParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ConversationParticipant
        fields = ("id", "user")


class ConversationSerializer(serializers.ModelSerializer):
    users = ConversationParticipantSerializer(many=True)

    class Meta:
        model = Conversation
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    conversation_participant = ConversationParticipantSerializer()
    class Meta:
        model = Message
        fields = "__all__"
