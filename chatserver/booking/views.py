from rest_framework import permissions, decorators
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

from rest_framework.viewsets import ModelViewSet

from .serializers import BookingSerializer, EventTypeSerializer
from .services.slots import get_available_slots
from .models import EventType, Booking


@api_view(['GET'])
def available_slots(request, username, event_slug):
    """
    Возвращает доступные временные слоты для выбранного типа события
    """
    event = EventType.objects.get(slug=event_slug, owner__username=username)
    date_str = request.query_params.get("date")  # например: ?date=2025-10-17
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    slots = get_available_slots(event, date, event.duration_minutes)
    return Response({"date": date_str, "slots": slots})


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all().select_related('guest', 'event_type')
    serializer_class = BookingSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        serializer.save(guest=self.request.user)


class EventTypeViewSet(ModelViewSet):
    queryset = EventType.objects.all().select_related('owner')
    serializer_class = EventTypeSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

