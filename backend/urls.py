from django.urls import path, include
from rest_framework import routers

from .views import (
    UserViewSet,
    BusinessViewSet,
    BusinessAutoCompleteView,
    TagViewSet,
    CategoryView,
    CategoryListView,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"businesses", BusinessViewSet, basename="business")
router.register(
    r"tags", TagViewSet,
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "businesses/autocomplete",
        BusinessAutoCompleteView.as_view(),
        name="business-autocomplete",
    ),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>/", CategoryView.as_view(), name="category-detail"
    ),
    path(
        "categories/<str:slug>/",
        CategoryView.as_view(),
        name="category-detail",
    ),
]
