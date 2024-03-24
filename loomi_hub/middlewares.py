import jwt
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.conf import settings


@database_sync_to_async
def get_user_from_jwt(token_key):
    try:
        payload = jwt.decode(token_key, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        return get_user_model().objects.get(id=user_id)
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidTokenError,
        get_user_model().DoesNotExist,
    ):
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            token_name, token_key = headers[b"authorization"].decode().split()
            if token_name == "Bearer":  # JWTs geralmente usam o prefixo 'Bearer'
                scope["user"] = await get_user_from_jwt(token_key)
        return await super().__call__(scope, receive, send)
