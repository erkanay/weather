import requests
from urllib.parse import urljoin

from django.conf import settings


class LocationIQClient:
    def __init__(self):
        self.base_url = settings.LOCATIONIQ_API_URL
        self.api_token = settings.LOCATIONIQ_TOKEN

    def get_points_by_location(self, location):
        """used to list information by location

        :param location:
        :return:
        """
        endpoint = "search.php?key={api_token}&q={location}&format=json".format(
            api_token=self.api_token,
            location=location
        )
        response = requests.get(urljoin(self.base_url, endpoint)).json()
        if not response:
            return None, None
        return response[0]["lat"], response[0]["lon"]
