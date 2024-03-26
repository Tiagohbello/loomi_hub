from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView

from loomi_hub.configuration.default_schema import Request
from loomi_hub.user.apis.serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)
from loomi_hub.user.models import User


class SignUpView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ["post"]


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    user = None
    my_tags = ['authentication']

    def post(self, request: Request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefrashView(TokenRefreshView):
    my_tags = ['authentication']

    def post(self, request: Request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    http_method_names = ["patch", "delete"]


class ChangePasswordView(APIView):
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = request.user

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"mensagem": "Password changed!"}, status=status.HTTP_200_OK
        )
