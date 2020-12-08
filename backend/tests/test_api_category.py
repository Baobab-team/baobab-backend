from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from users.models import CustomUser
from ..models import Category
from ..serializers import CategorySerializer


class TestCategoryEndpoint(APITestCase):
    url = reverse("category-list")

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="jojo@mail.com", password="bizzare"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Restaurant")

    def test_get_all(self):
        response = self.client.get(self.url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        response = self.client.get(
            reverse("category-detail", kwargs={"pk": 1})
        )
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Restaurant",
                "slug": "restaurant",
                "children": [],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        response = self.client.put(
            reverse("category-detail", kwargs={"pk": 1}),
            {"id": 1, "name": "jojo"},
        )
        self.assertEqual(
            json.loads(response.content),
            {"id": 1, "name": "jojo", "slug": "jojo", "children": []},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("jojo", Category.objects.get(name="jojo").name)
