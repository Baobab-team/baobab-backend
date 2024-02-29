from django.urls import path

from ..views import (

    BusinessView,
    BusinessListView,
    BusinessSuggestionListView,
    BusinessSuggestionView,
)

urlpatterns = [
    path("", BusinessListView.as_view(), name="business-list"),
    path(
        "<int:pk>/", BusinessView.as_view(), name="business-detail"
    ),
    path(
        "<str:slug>/",
        BusinessView.as_view(),
        name="business-detail",
    ),
    path(
        "suggestions/",
        BusinessSuggestionListView.as_view(),
        name="business-suggestion-list",
    ),
    path(
        "suggestions/<int:pk>/",
        BusinessSuggestionView.as_view(),
        name="business-suggestion-detail",
    ),


]
