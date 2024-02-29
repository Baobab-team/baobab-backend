from django.urls import path, include
from rest_framework import routers

from users.views import UserRegistrationView, UserLoginView

router = routers.DefaultRouter()

urlpatterns = [
    path(
        "auth/register/",
        UserRegistrationView.as_view(),
        name="user-register",
    ), path(
        "auth/login/",
        UserLoginView.as_view(),
        name="user-login",
    ),
]