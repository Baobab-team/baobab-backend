import logging
from datetime import datetime

import textdistance
from django.db.models import Q
from rest_framework import viewsets, status, filters, generics
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

from backend.models import Category, Business, Tag, BusinessSuggestion
from backend.pagination import DefaultPagination
from backend.serializers import (
    UserSerializer,
    CategorySerializer,
    BusinessSerializer,
    TagSerializer,
    SuggestionSerializer,
)
from users.models import CustomUser

logger = logging.getLogger(__name__)


class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if field in self.kwargs:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CategoryView(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_fields = ["pk", "slug"]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ["id", "name"]
    ordering = ["name"]

    def get_queryset(self):
        self.queryset = Category.objects.all()

        if self.request.query_params.get(
            "only_root", True
        ):  # temporary not optimal
            self.queryset = self.queryset.filter(parent__isnull=True)

        return self.queryset


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = DefaultPagination
    ordering_fields = ["id", "name"]
    ordering = ["name"]


class BusinessListView(MultipleFieldLookupMixin, generics.ListAPIView):
    serializer_class = BusinessSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "tags__name"]
    filterset_fields = ["status", "accepted_at", "category"]
    pagination_class = DefaultPagination
    ordering_fields = ["id", "name"]
    ordering = ["name"]
    lookup_fields = ["pk", "slug"]

    def get_queryset(self):
        exclude_deleted = self.request.query_params.get(
            "exclude_deleted", True
        )
        status = self.request.query_params.get("status", "accepted")
        category = self.request.query_params.get("category", None)
        location = self.request.query_params.get("location", None)
        accepted_at_after = self.request.query_params.get("accepted_at_after", None)

        self.queryset = Business.objects.all()
        self.queryset = self.queryset.filter(status=status)

        if exclude_deleted:
            self.queryset = self.queryset.exclude(deleted_at__isnull=False)
        if location:
            self.queryset = self.queryset.filter(addresses__city__icontains=location)
        if category:
            category_obj = Category.objects.get(slug=category)
            if category_obj:
                self.queryset = self.queryset.filter(
                    category__pk__in=category_obj.get_children_ids()
                )
        if accepted_at_after:
            formatted_date = datetime.strptime(accepted_at_after, '%Y-%m-%d')
            self.queryset = self.queryset.filter(accepted_at__gte=formatted_date.date())

        return self.queryset


class BusinessView(MultipleFieldLookupMixin, generics.RetrieveUpdateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    lookup_fields = ["pk", "slug"]


class BusinessAutoCompleteView(ListAPIView):
    def get_queryset(self):
        exclude_deleted = self.request.query_params.get(
            "exclude_deleted", False
        )
        status = self.request.query_params.get("status", None)
        self.queryset = Business.objects.all()

        if exclude_deleted:
            self.queryset = self.queryset.exclude(deleted_at__isnull=False)
        if status is None:
            self.queryset = self.queryset.filter(status="accepted")
        return self.queryset

    def list(self, request, *args, **kwargs):
        search = request.query_params.get("querySearch", None)
        distance = request.query_params.get("distance", 0.35)
        limit = request.query_params.get("limit", 10)

        if search is None:
            response = Response(
                {"message": "Missing query search parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            return response

        full_business_list = self.get_queryset()
        search_matching_business_list = self.get_queryset().filter(
            Q(name__contains=search) | Q(tags__name__contains=search)
        )

        matching_words = set([])
        for b in full_business_list:
            keyword = search.lower()
            matching_name = (
                textdistance.levenshtein.normalized_distance(
                    b.name.lower(), keyword
                )
                < distance
            )

            if matching_name:
                matching_words.add(b.name)

            for tag in b.tags.all():
                matching_tag = (
                    textdistance.levenshtein.normalized_distance(
                        tag.name.lower(), keyword
                    )
                    < distance
                )
                if matching_tag:
                    matching_words.add(tag.name)

        for b in search_matching_business_list:
            matching_words.add(b.name)

        matching_words = list(matching_words)[0:limit]
        response = Response(matching_words, status=status.HTTP_200_OK)
        return response


class BusinessSuggestionListView(
    generics.ListCreateAPIView, generics.RetrieveAPIView
):
    queryset = BusinessSuggestion.objects.all()
    serializer_class = SuggestionSerializer


class BusinessSuggestionView(generics.RetrieveAPIView):
    queryset = BusinessSuggestion.objects.all()
    serializer_class = SuggestionSerializer
