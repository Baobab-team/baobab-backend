from rest_framework import serializers

from backend.models import Category, Business, Tag
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class BusinessSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Business
        fields = [
            "category",
            "name",
            "description",
            "slogan",
            "website",
            "email",
            "status",
            "tags",
        ]
