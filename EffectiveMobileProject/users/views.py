import time
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .permissions import RolePermission

User = get_user_model()


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data
        if data.get("password") != data.get("password_repeat"):
            return Response({"error": "Пароли не совпадают"}, status=status.HTTP_400_BAD_REQUEST)

        user = Users.objects.create_user(
            email=data["email"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"]
        )
        return Response({"message": "Пользователь создан"})


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = Users.objects.get(email=email)
        except:
            return Response({"Ошибка": "Некорректные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"Ошибка": "Некорректные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"Ошибка": "Пользователь удален"}, status=status.HTTP_403_FORBIDDEN)

        payload = {
            "user_id": user.id,
            "exp": int(time.time()) + 24 * 3600,
            "iat": int(time.time()),
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return Response({"token": token})


class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Вы вышли"})


class UpdateProfileView(APIView):
    def put(self, request):
        user = request.user
        data = request.data

        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.patronymic = data.get("patronymic", user.patronymic)
        user.save()
        return Response({"message": "Профиль обновлен"})


class DeleteUserView(APIView):
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "Пользователь удален"})


class MockBusinessObjectsView(APIView):
    business_element = "users"

    permission_classes = [RolePermission]

    def get(self, request):
        return Response([
            {"id": 1, "name": "Объект A"},
            {"id": 2, "name": "Объект B"},
        ])