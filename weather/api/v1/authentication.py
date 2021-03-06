from rest_framework.authentication import TokenAuthentication


class WeatherTokenAuthentication(TokenAuthentication):
    keyword = 'Token'
