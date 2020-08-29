from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, CategoryViewSet, BusinessViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"categories", CategoryViewSet)
router.register(
    r"business", BusinessViewSet,
)

urlpatterns = [
    path("api/", include(router.urls)),
    # path('api/business/search/', BusinessSearchView.as_view(),{"name": "res"},name="business-search"),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
]
