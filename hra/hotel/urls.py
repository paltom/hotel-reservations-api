from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter

from hotel import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
