import requests
from urllib.parse import urljoin

from django.conf import settings


class DarkSkyClient:
    def __init__(self):
        self.base_url = settings.DARKSKY_API_URL
        self.api_token = settings.DARKSKY_TOKEN
        self.weather_info = {}

    def get_weather_info_by_points(self, lat, lon):
        """used to list information by location

        :param lat:
        :param lon:
        :return:
        """
        endpoint = "forecast/{api_token}/{lat},{lon}".format(
            api_token=self.api_token,
            lat=lat,
            lon=lon
        )
        response = requests.get(urljoin(self.base_url, endpoint)).json()
        if not response:
            return {}
        self.weather_info = response
        return response

    def current_temperature(self):
        return self.weather_info["currently"]["temperature"]

    def daily_low_and_high_temperatures(self):
        data = sorted(self.weather_info["hourly"]["data"], key=lambda k: k["temperature"])
        return dict(temperatureLow=data[0]["temperature"], temperatureHigh=data[-1]["temperature"])

    def weekly_low_and_high_temperatures(self):
        result = []
        for data in self.weather_info["daily"]["data"]:
            result.append(
                dict(
                    time=data["time"],
                    temperatureHigh=data["temperatureHigh"],
                    temperatureLow=data["temperatureLow"]
                )
            )
        return result

    def get_result(self):
        return dict(
            current_temperature=self.current_temperature(),
            daily_low_and_high_temperatures=self.daily_low_and_high_temperatures(),
            weekly_low_and_high_temperatures=self.weekly_low_and_high_temperatures()
        )
