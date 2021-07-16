from json import dumps, loads

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils.translation import gettext as _

from backend.models import BusinessSuggestion, Category, BaseModel, Business
from users.models import CustomUser


class TestSuggestionEndpoint(APITestCase):
    maxDiff = None

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="jojo@mail.com", password="bizzare"
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Restaurant")
        self.suggestion1 = BusinessSuggestion.objects.create(
            name="john",
            email="john.doe@email.com",
            is_owner=True,
            business=Business.objects.create(
                name="gracia afrika",
                category=self.category,
            ),
        )

    def test_get_all(self):
        response = self.client.get(reverse("business-suggestion-list"))
        self.assertEqual(
            to_dict(response.data),
            [
                {
                    "id": 1,
                    "name": "john",
                    "email": "john.doe@email.com",
                    "is_owner": True,
                    "business": {
                        "id": 1,
                        "name": "gracia afrika",
                        "description": "",
                        "website": "",
                        "email": "",
                        "phones": [],
                        "category": {
                            "name": "Restaurant",
                            "slug": "restaurant",
                            "children": [],
                            "id": 1,
                        },
                    },
                }
            ],
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_id(self):
        response = self.client.get(
            reverse("business-suggestion-detail", kwargs={"pk": 1})
        )
        self.assertEqual(
            to_dict(response.data),
            {
                "id": 1,
                "name": "john",
                "email": "john.doe@email.com",
                "is_owner": True,
                "business": {
                    "id": 1,
                    "name": "gracia afrika",
                    "description": "",
                    "website": "",
                    "email": "",
                    "phones": [],
                    "category": {
                        "name": "Restaurant",
                        "slug": "restaurant",
                        "children": [],
                        "id": 1,
                    },
                },
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        response = self.client.post(
            reverse("business-suggestion-list"),
            {
                "name": "john",
                "email": "john@mail.com",
                "business": {
                    "name": "bus1",
                    "phones": [{"number": "514-754-5588", "type": "tel"}],
                    "category": {"id": 1, "name": "Restaurant"},
                },
            },
            format="json",
        )
        self.assertEqual(
            to_dict(response.data),
            {
                "id": 2,
                "name": "john",
                "email": "john@mail.com",
                "is_owner": False,
                "business": {
                    "id": 2,
                    "name": "bus1",
                    "description": "",
                    "website": "",
                    "email": "",
                    "phones": [
                        {
                            "id": 1,
                            "number": "514-754-5588",
                            "type": "tel",
                            "extension": None,
                        }
                    ],
                    "category": {
                        "name": "Restaurant",
                        "slug": "restaurant",
                        "children": [],
                        "id": 1,
                    },
                },
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_not_existing_category(self):
        response = self.client.post(
            reverse("business-suggestion-list"),
            {
                "name": "john",
                "email": "john@mail.com",
                "business": {
                    "name": "bus1",
                    "phones": [],
                    "category": {"id": 10, "name": "unknown"},
                },
            },
            format="json",
        )
        self.assertEqual(response.data.get("code"), 400)
        self.assertEqual(response.data.get("message"), _("Unknown category"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


def custom_serializer(obj):
    if isinstance(obj, BaseModel):
        return obj.__dict__
    else:
        # Will get into this if the value is not serializable by default
        # and is also not a Name class object
        return None


def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict, default=custom_serializer))
