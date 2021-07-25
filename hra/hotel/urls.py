from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter

from hotel import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = [
    path('', include(router.urls))
]
