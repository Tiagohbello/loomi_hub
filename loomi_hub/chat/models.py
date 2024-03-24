import uuid

from django.core.exceptions import ValidationError
from django.db import models

from loomi_hub.user.models import User


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_group_status(self):
        """
        Update is_group status based on number of participants.
        """
        participant_count = (
            self.users.count()
        )
        if participant_count > 1 and not self.is_group:
            self.is_group = True
            self.save()


class ConversationParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="users"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.conversation}"

    def save(self, *args, **kwargs):
        """
        Override the save method to update the Conversation's is_group status when necessary.
        """
        super(ConversationParticipant, self).save(*args, **kwargs)
        self.conversation.update_group_status()


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    conversation_participant = models.ForeignKey(
        ConversationParticipant, on_delete=models.PROTECT, related_name="messages"
    )

    created_at = models.DateTimeField(auto_now_add=True)
