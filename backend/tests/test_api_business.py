from datetime import datetime
from json import loads, dumps

from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.utils import reverse_querystring
from users.models import CustomUser
from ..models import (
    Business,
    Category,
    Tag,
    BaseModel,
    SocialLink,
    Phone,
    Address,
    OpeningHour,
)
from ..serializers import BusinessSerializer


class TestBusinessEndpoint(APITestCase):
    url = reverse("business-list")
    maxDiff = None

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="jojo@mail.com", password="bizzare"
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Restaurant")
        self.tag = Tag.objects.create(name="africain")
        self.tag2 = Tag.objects.create(name="tag2")
        self.now = timezone.now()
        self.business = Business.objects.create(
            name="gracia afrika",
            category=self.category,
            status="accepted",
            created_at=self.now,
            updated_at=self.now,
        )
        self.business2 = Business.objects.create(
            name="restaurant2",
            category=self.category,
            status="accepted",
            created_at=self.now,
            updated_at=self.now,
        )
        self.business3 = Business.objects.create(
            name="business3",
            category=self.category,
            status="accepted",
            created_at=self.now,
            updated_at=self.now,
        )
        self.business.tags.add(self.tag)
        self.business.save()
        self.business2.tags.add(self.tag2)
        self.phone1 = Phone.objects.create(
            number="514-555-5555", type="tel", business=self.business3
        )
        self.social_link1 = SocialLink.objects.create(
            link="www.facebook.com/moi", business=self.business3
        )
        self.address1 = Address.objects.create(
            street_number="123",
            street_name="Wall Street",
            province="qc",
            business=self.business3,
        )
        self.business_hours = OpeningHour.objects.create(
            business=self.business3,
            day=1,
            opening_time=datetime(2020, 1, 1, 10, 0, 0),
            closing_time=datetime(2020, 1, 1, 17, 0, 0),
        )

    def test_get_all(self):
        response = self.client.get(self.url)
        businesses = Business.objects.all()
        serializer = BusinessSerializer(businesses, many=True)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail(self):
        response = self.client.get(
            reverse("business-detail", kwargs={"pk": 3}), format="json"
        )
        self.assertDictContainsSubset(
            {
                "id": 3,
                "category": {
                    "id": 1,
                    "name": "Restaurant",
                    "slug": "restaurant",
                    "children": [],
                },
                "name": "business3",
                "slug": "business3",
                "description": "",
                "email": "",
                "slogan": "",
                "status": "accepted",
                "tags": [],
                "website": "",
                "deleted_at": None,
                "accepted_at": None,
                "phones": [
                    {
                        "extension": None,
                        "id": 1,
                        "number": "514-555-5555",
                        "type": "tel",
                    }
                ],
                "addresses": [
                    {
                        "app_office_number": "",
                        "city": "Montreal",
                        "direction": "",
                        "id": 1,
                        "postal_code": "",
                        "province": "qc",
                        "street_name": "Wall Street",
                        "street_number": 123,
                        "street_type": "",
                    }
                ],
                "business_hours": [
                    {
                        "closing_time": "17:00:00",
                        "day": 1,
                        "id": 1,
                        "opening_time": "10:00:00",
                        "closed": False,
                    }
                ],
                "social_links": [
                    {
                        "id": 1,
                        "link": "www.facebook.com/moi",
                        "type": "facebook",
                    }
                ],
                "payment_types": [],
            },
            to_dict(response.data),
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
        self.assertDictContainsSubset(
            {
                "category": {
                    "id": 1,
                    "name": "Restaurant",
                    "slug": "restaurant",
                    "children": [],
                },
                "id": 1,
                "name": "jojo",
                "slug": "jojo",
                "description": "",
                "email": "",
                "slogan": "",
                "status": "accepted",
                "tags": [{"id": 1, "name": "africain"}],
                "addresses": [],
                "phones": [],
                "social_links": [],
                "business_hours": [],
                "website": "",
                "deleted_at": None,
                "accepted_at": None,
                "payment_types": [],
            },
            to_dict(response.data),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("jojo", Business.objects.get(name="jojo").name)

    #
    def test_search(self):
        url = reverse_querystring(
            "business-list", query_kwargs={"querySearch": "res"}
        )
        response = self.client.get(url, format="json",)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(
            {
                "category": {
                    "id": 1,
                    "name": "Restaurant",
                    "slug": "restaurant",
                    "children": [],
                },
                "id": 2,
                "name": "restaurant2",
                "slug": "restaurant2",
                "description": "",
                "email": "",
                "slogan": "",
                "status": "accepted",
                "tags": [{"id": 2, "name": "tag2"}],
                "phones": [],
                "addresses": [],
                "social_links": [],
                "business_hours": [],
                "website": "",
                "deleted_at": None,
                "accepted_at": None,
                "payment_types": [],
            },
            to_dict(response.data["results"][0]),
        )


def custom_serializer(obj):
    if isinstance(obj, BaseModel):
        return obj.__dict__
    else:
        # Will get into this if the value is not serializable by default
        # and is also not a Name class object
        return None


def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict, default=custom_serializer))
