from json import loads, dumps

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.utils import reverse_querystring
from users.models import CustomUser
from ..models import Business, Category, Tag, BaseModel
from ..serializers import BusinessSerializer


class TestBusinessEndpoint(APITestCase):
    url = reverse("business-list")

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="jojo@mail.com", password="bizzare"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Restaurant")
        self.tag = Tag.objects.create(name="africain")
        self.tag2 = Tag.objects.create(name="tag2")
        self.business = Business.objects.create(
            name="gracia afrika", category=self.category
        )
        self.business2 = Business.objects.create(
            name="restaurant2", category=self.category
        )
        self.business.tags.add(self.tag)
        self.business.save()
        self.business2.tags.add(self.tag2)

    def test_get_all(self):
        response = self.client.get(self.url)
        businesses = Business.objects.all()
        serializer = BusinessSerializer(businesses, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #
    def test_get_detail(self):
        response = self.client.get(
            reverse("business-detail", kwargs={"pk": 1}), format="json"
        )
        self.assertDictEqual(
            to_dict(response.data),
            {
                "id": 1,
                "category": {"id": 1, "name": "Restaurant"},
                "name": "gracia afrika",
                "description": "",
                "email": "",
                "slogan": "",
                "status": "pending",
                "tags": [{"id": 1, "name": "africain"}],
                "website": "",
                "deleted_at": None,
                "accepted_at": None,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #
    def test_put(self):
        response = self.client.put(
            reverse("business-detail", kwargs={"pk": 1}),
            {
                "id": 1,
                "name": "jojo",
                "category": {"id": 1, "name": "Restaurant"},
                "tags": {"id": 2, "name": "tag2"},
            },
            format="json",
        )
        self.assertDictEqual(
            to_dict(response.data),
            {
                "category": {"id": 1, "name": "Restaurant"},
                "id": 1,
                "name": "jojo",
                "description": "",
                "email": "",
                "slogan": "",
                "status": "pending",
                "tags": [{"id": 1, "name": "africain"}],
                "website": "",
                "deleted_at": None,
                "accepted_at": None,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("jojo", Business.objects.get(name="jojo").name)

    #
    def test_search(self):
        url = reverse_querystring(
            "business-list", query_kwargs={"search": "res"}
        )
        response = self.client.get(url, format="json",)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            to_dict(response.data["results"]),
            [
                {
                    "category": {"id": 1, "name": "Restaurant"},
                    "id": 2,
                    "name": "restaurant2",
                    "description": "",
                    "email": "",
                    "slogan": "",
                    "status": "pending",
                    "tags": [{"id": 2, "name": "tag2"}],
                    "website": "",
                    "deleted_at": None,
                    "accepted_at": None,
                },
            ],
        )

    def test_tags_put(self):
        response = self.client.put(
            reverse_querystring("business-tags", args=["1"]), {"names": "tag2"}
        )
        self.assertEqual(
            to_dict(response.data),
            [{"id": 1, "name": "africain"}, {"id": 2, "name": "tag2"}],
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tags_delete(self):
        response = self.client.delete(
            reverse_querystring("business-tags", args=["1"]), {"ids": "1,2"}
        )
        self.assertEqual(
            to_dict(response.data), [],
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_autocomplete(self):
        response = self.client.get(
            reverse_querystring("business-autocomplete"), {"search": "re"}
        )
        self.assertEqual(to_dict(response.data), ["restaurant2"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


def custom_serializer(obj):
    if isinstance(obj, BaseModel):
        return obj.__dict__
    else:
        # Will get into this if the value is not serializable by default
        # and is also not a Name class object
        return None


def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict, default=custom_serializer))
