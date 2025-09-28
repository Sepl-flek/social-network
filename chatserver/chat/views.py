from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet

from chat.models import Room
from chat.serializers import RoomSerializer


def index(request):
    return render(request, 'chat/index.html')


@login_required
def room(request, room_name):
    room_obj = get_object_or_404(Room, name=room_name)

    if not room_obj.users.filter(id=request.user.id).exists() and room_obj.owner.id != request.user.id:
        return HttpResponseForbidden("У вас нет прав доступа сюда😒")

    return render(request, 'chat/room.html', {'room_name': room_name})


class RoomsViewsSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
