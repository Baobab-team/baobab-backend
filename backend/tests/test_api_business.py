from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from users.models import CustomUser
from ..models import Business, Category
from ..serializers import BusinessSerializer


class TestBusinessEndpoint(APITestCase):
    url = reverse("business-list")

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="jojo@mail.com", password="bizzare"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Restaurant")
        self.business = Business.objects.create(
            name="gracia afrika", category=self.category
        )

    def test_get_all(self):
        response = self.client.get(self.url)
        businesses = Business.objects.all()
        serializer = BusinessSerializer(businesses, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        response = self.client.get(
            reverse("business-detail", kwargs={"pk": 1})
        )
        self.assertEqual(
            json.loads(response.content),
            {
                "category": {"id": 1, "name": "Restaurant"},
                "name": "gracia afrika",
                "description": "",
                "email": "",
                "slogan": "",
                "status": "pending",
                "tags": [],
                "website": "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        response = self.client.put(
            reverse("business-detail", kwargs={"pk": 1}),
            {
                "id": 1,
                "name": "jojo",
                "category": {"id": 1, "name": "Restaurant"},
            },
            format="json",
        )
        self.assertEqual(
            json.loads(response.content),
            {
                "category": {"id": 1, "name": "Restaurant"},
                "name": "jojo",
                "description": "",
                "email": "",
                "slogan": "",
                "status": "pending",
                "tags": [],
                "website": "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("jojo", Business.objects.get(name="jojo").name)
