from rest_framework.viewsets import ModelViewSet

from hotel.exceptions import RoomDeleteError
from hotel.models import Reservation, Room
from hotel.serializers import ReservationSerializer, RoomSerializer


class RoomViewSet(ModelViewSet):
    """
    Viewset providing endpoints for handling Rooms.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def destroy(self, request, pk: str):
        if Reservation.objects.filter(rooms__number__contains=pk).count():
            raise RoomDeleteError()
        return super().destroy(request, pk)


class ReservationViewSet(ModelViewSet):
    """
    Viewset providing endpoints for handling Reservations.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
