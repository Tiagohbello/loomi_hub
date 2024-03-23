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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "put", "delete"]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        if post_id:
            return Comment.objects.filter(post__id=post_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post_id"] = self.kwargs.get("post_id")
        return context


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        if post_id:
            return Like.objects.filter(post__id=post_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["post_id"] = self.kwargs.get("post_id")
        return context
