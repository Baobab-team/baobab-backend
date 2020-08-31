from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from users.models import CustomUser
from ..models import Business, Category, Tag
from ..serializers import BusinessSerializer
from ..views import BusinessViewSet


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

    def test_get_detail(self):
        response = self.client.get(
            reverse("business-detail", kwargs={"pk": 1})
        )
        self.assertEqual(
            response.data,
            {
                "category": {"id": 1, "name": "Restaurant"},
                "id": 1,
                "name": "gracia afrika",
                "description": "",
                "email": "",
                "slogan": "",
                "status": "pending",
                "tags": [{"id": 1, "name": "africain"}],
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
                "tags": {"id": 2, "name": "tag2"},
            },
            format="json",
        )
        self.assertEqual(
            response.data,
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
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("jojo", Business.objects.get(name="jojo").name)

    def test_get_with_filter(self):
        url = reverse("business-list")
        query_param = "name__icontains=res"
        full_url = f"{url}?{query_param}"
        response = self.client.get(full_url, format="json",)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
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
                },
            ],
        )

    def test_get_with_filter2(self):
        url = reverse("business-list")
        query_param = "tags__name__icontains=tag2"
        full_url = f"{url}?{query_param}"
        response = self.client.get(full_url, format="json",)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
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
                }
            ],
        )

    # def test_tags_post(self):
    #     # view = BusinessViewSet.as_view({'get': 'tags'})
    #     response = self.client.post(
    #         reverse('business-tags',args=['1']),
    #         {"id": 2, "name": "tag2"},
    #     )
    #     # factory = APIRequestFactory()
    #     # request = factory.post('/api/business/1/tags', {"id": 2, "name": "tag2"}, format='json')
    #     # response = view(request)
    #     # response.render()
    #     self.assertEqual(
    #         response.data,
    #
    #             # "category": {"id": 1, "name": "Restaurant"},
    #             # "id": 1,
    #             # "name": "gracia afrika",
    #             # "description": "",
    #             # "email": "",
    #             # "slogan": "",
    #             # "status": "pending",
    #              [{"id": 1, "name": "africain"}, {"id": 2, "name": "tag2"}],
    #             # "website": "",
    #
    #
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
