from urllib.parse import urljoin

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class CompetitionViewTests(APITestCase):
    def setUp(self):
        self.params = {
            "category": "pizza",
            "lat": 51.50,
            "lon": -0.13,
            "country_code": "UK"
        }

    def get_competition_info_url(self, **params):
        self.url_params = "?category={category}&lat={lat}&lon={lon}&country_code={country_code}".format(**params)
        return urljoin(reverse("competitions-get-competition-info"), self.url_params)

    def test_success_get_competition_info(self):
        response = self.client.get(self.get_competition_info_url(**self.params), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_get_competition_info_for_not_allowed_country(self):
        self.params["country_code"] = "US"
        response = self.client.get(self.get_competition_info_url(**self.params), format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_competition_info_for_not_allowed_length_name(self):
        self.params["category"] = "over 20 chars chars chars chars"
        response = self.client.get(self.get_competition_info_url(**self.params), format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
