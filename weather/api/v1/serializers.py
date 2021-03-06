from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

from weather.app.models import WeatherReportHistory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password", "token",)

    @staticmethod
    def get_token(obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "is_active",)


class WeatherReportHistorySerializer(serializers.ModelSerializer):
    result = serializers.ReadOnlyField()

    class Meta:
        model = WeatherReportHistory
        fields = ("location", "result",)

    def validate(self, attrs):
        if not attrs["location"]:
            raise serializers.ValidationError({"location": ["location required."]})
        return attrs
