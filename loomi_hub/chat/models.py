import uuid

from django.core.exceptions import ValidationError
from django.db import models

from loomi_hub.user.models import User


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_group = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="messages")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self):
        if not ConversationParticipant.objects.filter(
            user=self.user, conversation=self.conversation
        ):
            raise ValidationError(
                "This user cannot send a message to this conversation."
            )


class ConversationParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="users"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="conversations"
    )

    created_at = models.DateTimeField(auto_now_add=True)
