from rest_framework import serializers

from loomi_hub.post.models import Post, Comment
from loomi_hub.user.apis.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "created_at": {"read_only": True}}

    def validate(self, attrs):
        if not attrs.get("image") and not attrs.get("content"):
            raise serializers.ValidationError(
                "You must provide either an image or content."
            )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = (
            UserSerializer(instance.user).data if representation["user"] else None
        )
        return representation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "created_at": {"read_only": True},
            "user": {"read_only": True},
            "post": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context["request"].user
        post = Post.objects.filter(id=self.context["post_id"]).first()
        validated_data["user"] = user
        if post:
            validated_data["post"] = post
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = (
            UserSerializer(instance.user).data if representation["user"] else None
        )
        return representation
