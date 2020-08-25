from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
]
