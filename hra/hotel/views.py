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

    def partial_update(self, request, pk: int, **kwargs):
        # to satisfy validator, add rooms from reservation if they're not
        # getting updated
        if 'rooms' not in request.data:
            request.data.update({'rooms': [r['number'] for r in list(
                Reservation.objects.get(pk=pk).rooms.values('number').iterator())]})
        return super().partial_update(request, pk, **kwargs)
