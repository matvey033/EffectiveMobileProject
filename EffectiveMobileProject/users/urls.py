from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UpdateProfileView, DeleteUserView, MockBusinessObjectsView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("update/", UpdateProfileView.as_view()),
    path("delete/", DeleteUserView.as_view()),
    path("objects/", MockBusinessObjectsView.as_view()),
]
