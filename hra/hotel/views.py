from rest_framework.viewsets import ModelViewSet

from hotel.models import Reservation, Room
from hotel.serializers import ReservationSerializer, RoomSerializer


class RoomViewSet(ModelViewSet):
    """
    Viewset providing endpoints for handling Rooms.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ReservationViewSet(ModelViewSet):
    """
    Viewset providing endpoints for handling Reservations.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
