from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from backend.serializers import UserSerializer
from users.models import CustomUser


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
