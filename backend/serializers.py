from rest_framework import serializers

from backend.models import (
    Category,
    Business,
    Tag,
    Phone,
    Address,
    SocialLink,
    OpeningHour,
)
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


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        exclude = ["business", "created_at", "deleted_at", "updated_at"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["business", "created_at", "deleted_at", "updated_at"]


class SocialLinkSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class Meta:
        model = SocialLink
        exclude = ["business", "created_at", "deleted_at", "updated_at"]


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        exclude = ["business", "created_at", "deleted_at", "updated_at"]


class BusinessSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    phones = PhoneSerializer(read_only=True, many=True)
    social_links = SocialLinkSerializer(read_only=True, many=True)
    addresses = AddressSerializer(read_only=True, many=True)
    opening_hours = OpeningHourSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)
    accepted_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Business
        fields = [
            "id",
            "category",
            "name",
            "description",
            "slogan",
            "website",
            "email",
            "status",
            "tags",
            "phones",
            "addresses",
            "addresses",
            "social_links",
            "opening_hours",
            "deleted_at",
            "accepted_at",
        ]
