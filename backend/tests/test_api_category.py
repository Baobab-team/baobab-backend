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
        self.category2 = Category.objects.create(name="sous-restaurant")

    def test_get_all(self):
        response = self.client.get(self.url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_only_root(self):
        response = self.client.get(self.url + "?only_root=True")
        categories = Category.objects.filter(parent__isnull=True).all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        response = self.client.get(
            reverse("category-detail", kwargs={"pk": 1})
        )
        category = Category.objects.get(pk=1)
        serializer = CategorySerializer(category, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        response = self.client.put(
            reverse("category-detail", kwargs={"pk": 1}),
            {"id": 1, "name": "jojo"},
        )
        category = Category.objects.get(pk=1)
        serializer = CategorySerializer(category, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("jojo", category.name)
