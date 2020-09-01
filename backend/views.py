from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
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


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []  # TODO add permissions
    pagination_class = DefaultPagination
    ordering_fields = ["id", "name"]
    ordering = ["name"]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []  # TODO add permissions
    pagination_class = DefaultPagination
    ordering_fields = ["id", "name"]
    ordering = ["name"]


class BusinessViewSet(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    permission_classes = []  # TODO add permissions
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["name", "tags"]
    pagination_class = DefaultPagination
    ordering_fields = ["id", "name"]
    ordering = ["name"]

    def get_queryset(self):
        exclude_deleted = self.request.query_params.get("deleted_at", False)
        self.queryset = Business.objects.all()

        if exclude_deleted:
            self.queryset = self.queryset.exclude(deleted_at__isnull=False)
        return self.queryset

    @action(detail=True, methods=["PATCH"])
    def update_status(self, request, pk=None):
        business = self.get_object()
        new_status = request.query_params.get("status", None)

        if new_status:
            business.update_status(new_status)
            serializer = self.get_serializer(Business, partial=True)
            if serializer.is_valid():
                business.save()
                return Response(serializer.data)
            return Response(
                {"message": "Provide valid status"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "Provide valid status"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["PUT", "DELETE"])
    def tags(self, request, pk=None):
        business = self.get_object()
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            if request.method == "POST":
                business.save()
                tag.save()
                business.tags.add(tag)
            elif request.method == "DELETE":
                business.tags.remove(tag)
            business.save()
            serializer = TagSerializer(business.tags, many=True)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
