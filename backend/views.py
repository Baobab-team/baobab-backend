from django.http import HttpResponse
from rest_framework import viewsets, permissions

from backend.models import Category
from backend.serializers import UserSerializer, CategorySerializer
from users.models import CustomUser


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
