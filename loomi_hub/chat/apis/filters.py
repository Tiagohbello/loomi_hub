import django_filters
from django.db.models import Prefetch

from loomi_hub.chat.models import Conversation, Message, ConversationParticipant


class ConversationFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(method="filter_by_user", required=False)

    class Meta:
        model = Conversation
        fields = []

    def filter_by_user(self, queryset, name, value):
        return queryset.prefetch_related(
            Prefetch(
                "users", queryset=ConversationParticipant.objects.select_related("user")
            )
        ).filter(users__user_id=value)


class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.UUIDFilter(
        method="filter_by_conversation", required=False
    )

    class Meta:
        model = Message
        fields = []

    def filter_by_conversation(self, queryset, name, value):
        return queryset.prefetch_related(
            Prefetch(
                "conversation_participant",
                queryset=ConversationParticipant.objects.select_related("conversation"),
            )
        ).filter(conversation_participant__conversation_id=value)
