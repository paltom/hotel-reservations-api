from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet


DETAIL_ACTIONS = ['retrieve', 'update', 'partial_update', 'destroy']
LIST_ACTIONS = ['list', 'create']


def is_staff(user):
    return user.is_staff or user.groups.filter(
        name='staff').exists()


class UserViewSetPermissions(BasePermission):
    """
    Permissions for users endpoint.
    """

    def has_permission(self, request: Request, view: ModelViewSet):
        user = request.user
        method = request.method
        action = view.action
        if action in DETAIL_ACTIONS:
            # pass checking to has_object_permission
            return True
        if action in LIST_ACTIONS:
            if method == 'GET' and is_staff(user):
                # only admin and staff members can list users
                return True
            if method == 'POST' and (
                    user.is_anonymous or is_staff(user)):
                # only admin or anonymous users can add new user
                return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if is_staff(user):
            # staff member can do anything with user
            return True
        if user == obj:
            # user can do anything with themselves
            return True
        return False


class ReservationViewSetPermissions(BasePermission):
    """
    Permissions for reservations endpoint.
    """

    def has_permission(self, request: Request, view: ModelViewSet):
        user = request.user
        if user.is_anonymous:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if is_staff(user):
            # staff member can do anything with all reservations
            return True
        if obj.owner == user:
            # user can do anything with owned reservation
            return True
        return False


class RoomViewSetPermissions(BasePermission):
    """
    Permissions for rooms endpoint.
    """

    def has_permission(self, request: Request, view: ModelViewSet):
        user = request.user
        if user.is_anonymous:
            return False
        if view.action in ['list', 'retrieve']:
            # all users can list rooms
            return True
        if not is_staff(user):
            return False
        return True
