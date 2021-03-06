from datetime import datetime

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from django.core.cache import cache
from django.contrib.auth import get_user_model

from . import serializers
from weather.api import utils
from weather.app import models
from weather.integrations.darksky import DarkSkyClient
from weather.integrations.locationiq import LocationIQClient

User = get_user_model()


class UserSignupView(GenericViewSet, CreateModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(dict(token=token.key))


class WeatherView(GenericViewSet):
    serializer_class = serializers.WeatherReportHistorySerializer
    # permissions.IsAuthenticated may be used if it required
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=["get"])
    def get_weather_report(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        data = serializer.data.copy()
        location = data.get("location")

        key = "{}_{}".format(location, datetime.today().strftime("%d%m%Y"))

        cached_result = cache.get(key)
        if cached_result:
            return utils.http_ok_with_dict(cached_result)

        instance = models.WeatherReportHistory.objects.filter(
            location=location,
            created__date=datetime.today()
        ).first()

        if not instance:
            locationiq_client = LocationIQClient()
            lat, lon = locationiq_client.get_points_by_location(location)
            if not (lat and lon):
                return utils.http_not_found_with_details("points not found for this location.")

            darksky_client = DarkSkyClient()
            weather_info = darksky_client.get_weather_info_by_points(lat, lon)
            if not weather_info:
                return utils.http_not_found_with_details("weather info not found.")

            instance = models.WeatherReportHistory.objects.create(
                location=location,
                result=darksky_client.get_result()
            )

        serializer = self.serializer_class(instance=instance)
        return utils.http_ok_with_dict(serializer.data)
