from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
    TokenObtainPairView,
)

from loomi_hub.user.apis.viewsets import (
    SignUpView,
    LoginView,
    UserViewSet,
    ChangePasswordView, RefrashView,
)

drf_router = DefaultRouter()
drf_router.register(r"sign_up", SignUpView, basename="sign_up")
drf_router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("login/refresh/", RefrashView.as_view(), name="login_refresh"),
    path("password/change/", ChangePasswordView.as_view(), name="change_password"),
    path("", include(drf_router.urls)),
]
