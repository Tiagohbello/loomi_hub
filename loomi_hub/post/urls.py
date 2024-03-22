from django.urls import path, include
from rest_framework.routers import DefaultRouter

from loomi_hub.post.apis.viewsets import PostViewSet, CommentViewSet

drf_router = DefaultRouter()

drf_router.register(r"", PostViewSet, basename="post")


urlpatterns = [
    path(
        "<uuid:post_id>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comment",
    ),
    path(
        "<uuid:post_id>/comments/<uuid:pk>/",
        CommentViewSet.as_view(
            {"put": "update", "delete": "destroy"}
        ),
        name="comment-edit",
    ),
    path("", include(drf_router.urls)),
]
