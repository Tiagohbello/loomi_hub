import django_filters

from loomi_hub.chat.models import Conversation, Message


class ConversationFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(method="filter_by_user", required=True)

    class Meta:
        model = Conversation
        fields = []

    def filter_by_user(self, queryset, name, value):
        return queryset.filter(users__user_id=value)


class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.UUIDFilter(method="filter_by_conversation", required=True)

    class Meta:
        model = Message
        fields = []

    def filter_by_conversation(self, queryset, name, value):
        return queryset.filter(conversation_participant__conversation_id=value)
