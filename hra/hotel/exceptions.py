from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class RoomDeleteError(APIException):
    status_code = 400
    default_detail = 'Cannot delete room that has reservations.'
    default_code = 'bad_request'
