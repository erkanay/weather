from rest_framework import status
from rest_framework.response import Response

DETAILS_KEY = 'details'


def http_not_found_with_details(detail_message):
    return Response({DETAILS_KEY: detail_message}, status=status.HTTP_404_NOT_FOUND)


def http_ok_with_dict(dict_response=None):
    if dict_response:
        return Response(dict_response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)
