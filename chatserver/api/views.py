from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import RoomSerializer, MessageSerializer
from chat.models import Room, Message


# views that related with api
class RoomsViewsSet(ModelViewSet):
    queryset = Room.objects.select_related('owner').prefetch_related('users')
    serializer_class = RoomSerializer


class MessageListView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return Message.objects.filter(room__id=room_id).select_related('author')

