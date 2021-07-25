from datetime import timedelta

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models.expressions import F
from rest_framework.exceptions import ValidationError
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

    def get_queryset(self):
        """
        Provides searching capabilities.
        """
        queryset = super().get_queryset()
        if self.action == 'list':
            # do searching only in list view, not in detail view
            queryset = self._search_queryset(queryset)
        return queryset

    def _search_queryset(self, queryset):
        params = self.request.query_params
        if 'room_number' in params:
            queryset = queryset.filter(
                rooms__number=params['room_number'])
        if 'name' in params:
            queryset = queryset.filter(name__contains=params['name'])
        if 'date' in params:
            try:
                queryset = queryset.filter(
                    date_from__lte=params['date'],
                    date_to__gte=params['date'])
            except DjangoValidationError as e:
                raise ValidationError(e.message, e.code)
        if 'date_from' in params:
            try:
                queryset = queryset.filter(date_from=params['date_from'])
            except DjangoValidationError as e:
                raise ValidationError(e.message, e.code)
        if 'date_to' in params:
            try:
                queryset = queryset.filter(date_to=params['date_to'])
            except DjangoValidationError as e:
                raise ValidationError(e.message, e.code)
        if 'duration' in params:
            try:
                duration = int(params['duration'])
            except ValueError as e:
                raise ValidationError(e.__cause__)
            if duration < 1:
                raise ValidationError(
                    'reservation duration cannot be negative')
            queryset = queryset.filter(
                date_to=F('date_from') +
                timedelta(duration))
        return queryset
