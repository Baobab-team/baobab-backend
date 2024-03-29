from django.urls import path, include
from rest_framework import routers

from .views import (
    UserViewSet,
    BusinessView,
    BusinessListView,
    BusinessAutoCompleteView,
    TagViewSet,
    CategoryView,
    CategoryListView,
    BusinessSuggestionListView,
    BusinessSuggestionView,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
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
    path(
        "businesses/suggestions/",
        BusinessSuggestionListView.as_view(),
        name="business-suggestion-list",
    ),
    path(
        "businesses/suggestions/<int:pk>/",
        BusinessSuggestionView.as_view(),
        name="business-suggestion-detail",
    ),
    path("businesses/", BusinessListView.as_view(), name="business-list"),
    path(
        "businesses/<int:pk>/", BusinessView.as_view(), name="business-detail"
    ),
    path(
        "businesses/<str:slug>/",
        BusinessView.as_view(),
        name="business-detail",
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
