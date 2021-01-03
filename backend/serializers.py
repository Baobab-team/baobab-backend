from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.utils.translation import gettext as _

from backend.models import (
    Category,
    Business,
    Tag,
    Phone,
    Address,
    SocialLink,
    OpeningHour,
    PaymentType,
    Suggestion,
)
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email"]


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "children",
        ]

    slug = serializers.SlugField(read_only=True)
    children = RecursiveField(many=True, read_only=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
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
    payment_types = serializers.StringRelatedField(read_only=True, many=True)
    phones = PhoneSerializer(read_only=True, many=True)
    social_links = SocialLinkSerializer(read_only=True, many=True)
    addresses = AddressSerializer(read_only=True, many=True)
    business_hours = OpeningHourSerializer(
        read_only=True, many=True, source="opening_hours"
    )
    category = CategorySerializer(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)
    accepted_at = serializers.DateField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Business
        fields = [
            "id",
            "category",
            "name",
            "slug",
            "description",
            "slogan",
            "website",
            "email",
            "status",
            "tags",
            "phones",
            "addresses",
            "social_links",
            "business_hours",
            "deleted_at",
            "accepted_at",
            "created_at",
            "updated_at",
            "payment_types",
        ]


class BusinessCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    phones = PhoneSerializer(many=True, default=[])

    class Meta:
        model = Business
        fields = [
            "id",
            "name",
            "phones",
            "email",
            "website",
            "description",
            "category",
        ]


class SuggestionSerializer(serializers.ModelSerializer):
    business = BusinessCreateSerializer(many=False)

    class Meta:
        model = Suggestion
        fields = [
            "id",
            "email",
            "name",
            "business",
        ]

    def create(self, validated_data):
        business = validated_data.pop("business")
        category = business.pop("category")
        try:
            phones = business.pop("phones")
            category = Category.objects.get(name=category.get("name"))
            business = Business.objects.create(category=category, **business)
            for phone in phones:
                Phone.objects.create(business=business, **phone)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                detail={"message": _("Unknown category")}, code=400
            )
        return Suggestion.objects.create(business=business, **validated_data)
