from django.contrib import admin

from loomi_hub.chat.models import Conversation, Message, ConversationParticipant


class ConversationParticipantsInline(admin.TabularInline):
    model = ConversationParticipant
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_group",
    )
    inlines = [ConversationParticipantsInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("conversation_participant", "content")
