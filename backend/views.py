from django.http import HttpResponse
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend

from backend.models import Category, Business
from backend.serializers import (
    UserSerializer,
    CategorySerializer,
    BusinessSerializer,
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


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = []  # TODO add permissions
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["name", "tags"]
