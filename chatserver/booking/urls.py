from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BookingViewSet, available_slots

router = SimpleRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'event-type', BookingViewSet, basename='event-type')

urlpatterns = [
    # GET /api/booking/available-slots/<username>/<event_slug>/?date=2025-10-17
    path('available-slots/<str:username>/<str:event_slug>/', available_slots, name='available-slots'),

    path('', include(router.urls)),
]
