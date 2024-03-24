from rest_framework import serializers

from loomi_hub.chat.models import Conversation, ConversationParticipant, Message
from loomi_hub.user.apis.serializers import UserSerializer


class ConversationParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConversationParticipant
        fields = ("id", "user")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = (
            UserSerializer(instance.user).data if representation["user"] else None
        )
        return representation


class ConversationSerializer(serializers.ModelSerializer):
    users = ConversationParticipantSerializer(many=True)
    is_group = serializers.BooleanField(read_only=True)

    class Meta:
        model = Conversation
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    conversation_participant = ConversationParticipantSerializer()

    class Meta:
        model = Message
        fields = "__all__"
