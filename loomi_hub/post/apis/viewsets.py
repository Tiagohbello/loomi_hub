from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from loomi_hub.permissions import IsOwnerOrReadOnly
from loomi_hub.post.apis.serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
)
from loomi_hub.post.models import Post, Comment, Like
from loomi_hub.post.utils.notification_sender import send_notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at").select_related("user")
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "put", "delete"]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "put", "delete"]
    my_tags = ['comment']

    def get_queryset(self):
        queryset = self.queryset
        post_id = self.kwargs.get("post_id")
        if post_id:
            queryset = queryset.filter(post__id=post_id)
        return queryset.select_related("user", "post")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post_id"] = self.kwargs.get("post_id")
        return context


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "delete"]
    my_tags = ['like']

    def get_queryset(self):
        queryset = self.queryset
        post_id = self.kwargs.get("post_id")
        if post_id:
            queryset = queryset.filter(post__id=post_id)
        return queryset.select_related("user", "post")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post_id"] = self.kwargs.get("post_id")
        return context
