import datetime
from typing import Dict, Any

from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from loomi_hub.settings import SIMPLE_JWT
from loomi_hub.user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    expires_in = serializers.DateTimeField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    uuid = serializers.CharField(read_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data: Dict[str, Any] = super().validate(attrs)
        data = {
            "access": data["access"],
            "refresh": data["refresh"],
            "expires_in": datetime.datetime.now() + SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            "uuid": self.user.pk,
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("current_password", "new_password", "new_password_confirmation")

    def validate(self, data):
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        new_password_confirmation = data.get("new_password_confirmation")

        if new_password != new_password_confirmation:
            raise serializers.ValidationError(
                {"new_password_confirmation": "Passwords do not match"}
            )

        user = self.context["request"].user

        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": "Current password is not correct"}
            )

        if current_password == new_password:
            raise serializers.ValidationError(
                {"new_password": "New password must be different from old password"}
            )

        password_validation.validate_password(new_password, self.instance)

        return data