from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from api.serializers import RoomSerializer
from chat.models import Room


# views that related with api
class RoomsViewsSet(ModelViewSet):
    queryset = Room.objects.select_related('owner').prefetch_related('users')
    serializer_class = RoomSerializer
