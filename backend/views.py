import logging
import operator
from functools import reduce

import textdistance
from django.db.models import Q
from rest_framework import viewsets, status, filters, generics
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

from backend.models import Category, Business, Tag
from backend.pagination import DefaultPagination
from backend.serializers import (
    UserSerializer,
    CategorySerializer,
    BusinessSerializer,
    TagSerializer,
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


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = DefaultPagination
    ordering_fields = ["id", "name"]
    ordering = ["name"]


class BusinessViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "tags__name"]
    filterset_fields = ["status", "accepted_at", "category"]
    pagination_class = DefaultPagination
    ordering_fields = ["id", "name"]
    ordering = ["name"]

    def get_queryset(self):
        exclude_deleted = self.request.query_params.get(
            "exclude_deleted", None
        )
        status = self.request.query_params.get("status", None)
        category = self.request.query_params.get("category", None)
        self.queryset = Business.objects.all()

        if exclude_deleted:
            self.queryset = self.queryset.exclude(deleted_at__isnull=False)
        if status is None:
            self.queryset = self.queryset.filter(status="accepted")
        if category:
            self.queryset = self.queryset.filter(
                category__name__iexact=category
            )
        return self.queryset

    @action(detail=True, methods=["PATCH"])
    def update_status(self, request, pk=None):
        business = self.get_object()
        new_status = request.data.get("status", None)

        if new_status:
            business.update_status(new_status)
            serializer = self.get_serializer(
                business, {"status": new_status}, partial=True
            )
            if serializer.is_valid():
                business.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Please provide a status"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["PUT", "DELETE"])
    def tags(self, request, pk=None):
        business = self.get_object()
        tag_names = request.data.get("names", [])
        tags_id = request.data.get("ids", [])
        if not tag_names and not tags_id:
            return Response(
                {
                    "message": "Please provide a list of valid tags id or tags name"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if tag_names:
            tag_names = tag_names.split(",")
        else:
            tags_id = tags_id.split(",")
        tags = Tag.objects.filter(Q(name__in=tag_names) | Q(pk__in=tags_id))

        if request.method == "PUT":
            for tag in tags:
                business.tags.add(tag)
        elif request.method == "DELETE":
            for tag in tags:
                business.tags.remove(tag)
        business.save()
        serializer = TagSerializer(business.tags, many=True)
        return Response(serializer.data)


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
