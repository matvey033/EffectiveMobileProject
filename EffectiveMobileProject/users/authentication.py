import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("Неверный формат токена")

        if prefix.lower() != "bearer":
            raise AuthenticationFailed("Неверный префикс токена")

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Токен истек")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Неверный токен")

        try:
            user = User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            raise AuthenticationFailed("Пользователь не найден")

        if not user.is_active:
            raise AuthenticationFailed("Пользователь удален")

        return user, None