from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from loomi_hub.post.models import Post, Comment, Like
from loomi_hub.post.utils.notification_sender import send_notification
from loomi_hub.user.apis.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "created_at": {"read_only": True},
            "thumbnail": {"read_only": True},
        }

    def validate(self, attrs):
        if not attrs.get("image") and not attrs.get("content"):
            raise serializers.ValidationError(
                "You must provide either an image or content."
            )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        send_notification(f"{user.username} just added a post")
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
        validated_data["post"] = post
        send_notification(f"{user.username} just commented on a post")
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = (
            UserSerializer(instance.user).data if representation["user"] else None
        )
        return representation


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "post": {"read_only": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        post_id = self.context["post_id"]
        post = Post.objects.filter(id=post_id).first()

        # Verifique se o like já existe
        if Like.objects.filter(user=user, post=post).exists():
            raise ValidationError("The user already likes this post")

        validated_data["user"] = user
        validated_data["post"] = post
        send_notification(f"{user.username} just liked a post")
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["user"] = (
            UserSerializer(instance.user).data if representation["user"] else None
        )
        representation["post"] = (
            PostSerializer(instance.post).data if representation["post"] else None
        )

        return representation
