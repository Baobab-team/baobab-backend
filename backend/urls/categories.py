from django.urls import path

from ..views import (
    CategoryView,
    CategoryListView,
)

urlpatterns = [

    path("", CategoryListView.as_view(), name="category-list"),
    path(
        "<int:pk>/", CategoryView.as_view(), name="category-detail"
    ),
    path(
        "<str:slug>/",
        CategoryView.as_view(),
        name="category-detail",
    ),
]
