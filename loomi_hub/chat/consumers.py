from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .apis.serializers import MessageSerializer
from .models import ConversationParticipant, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["id"]
        self.user = self.scope["user"]
        if await self.is_user_in_conversation():
            await self.channel_layer.group_add(
                self.conversation_group_name(), self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.conversation_group_name(), self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if await self.is_user_in_conversation():
            serialized_data = await self.create_message(message)
            await self.channel_layer.group_send(
                self.conversation_group_name(),
                {"type": "chat.message", "serialized_data": serialized_data},
            )

    async def chat_message(self, event):
        message = json.dumps(
            event["serialized_data"]
        )  # Serialize dictionary to JSON string
        await self.send(text_data=message)

    @database_sync_to_async
    def is_user_in_conversation(self):
        return ConversationParticipant.objects.filter(
            conversation_id=self.conversation_id, user=self.user
        ).exists()

    @database_sync_to_async
    def create_message(self, content):
        conversation_participant = ConversationParticipant.objects.get(
            conversation_id=self.conversation_id, user=self.user
        )
        message = Message.objects.create(
            content=content, conversation_participant=conversation_participant
        )
        serializer = MessageSerializer(message)
        serialized_data = serializer.data
        return serialized_data

    def conversation_group_name(self):
        return f"conversation_{self.conversation_id}"
